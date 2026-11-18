from decimal import Decimal
from django.db import transaction as db_tx
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts_auth.views import IsBankOfficerOrAdmin
from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Transaction
from .models import LoanApplication, LoanProduct, LoanRepayment
from .serializers import (
    ApplyLoanSerializer,
    LoanApplicationSerializer,
    LoanProductSerializer,
    LoanRepaymentSerializer,
    ReviewLoanSerializer,
    compute_emi,
    disburse_loan_and_generate_schedule,
)


class LoanProductListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        products = LoanProduct.objects.filter(is_active=True)
        return Response(LoanProductSerializer(products, many=True).data, status=status.HTTP_200_OK)


class EMICalculatorView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            principal = Decimal(str(request.data.get('principal', '0')))
            rate = Decimal(str(request.data.get('interest_rate', '0')))
            tenure = int(request.data.get('tenure_months', 0))
            if principal <= 0 or tenure <= 0:
                raise ValueError
        except Exception:
            return Response(
                {'detail': 'Provide valid positive principal, interest_rate, and tenure_months.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        emi = compute_emi(principal, rate, tenure)
        total_payable = (emi * tenure).quantize(Decimal('0.01'))
        total_interest = (total_payable - principal).quantize(Decimal('0.01'))
        return Response(
            {
                'emi_amount': str(emi),
                'total_payable': str(total_payable),
                'total_interest': str(total_interest),
            },
            status=status.HTTP_200_OK,
        )


class LoanApplicationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role.role_code in ('ADMIN', 'BANK_OFFICER', 'AUDITOR'):
            qs = LoanApplication.objects.select_related('user', 'loan_product', 'disbursement_account').all()
        else:
            qs = LoanApplication.objects.select_related('user', 'loan_product', 'disbursement_account').filter(
                user=request.user
            )
        return Response(LoanApplicationSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ApplyLoanSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        loan = serializer.save()
        return Response(LoanApplicationSerializer(loan).data, status=status.HTTP_201_CREATED)


class LoanReviewView(APIView):
    permission_classes = [IsBankOfficerOrAdmin]

    def patch(self, request, loan_id):
        loan = get_object_or_404(LoanApplication, loan_id=loan_id)
        if loan.loan_status not in ('APPLIED', 'UNDER_REVIEW'):
            return Response(
                {'detail': f'Loan is already in {loan.loan_status} state.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ReviewLoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        decision = serializer.validated_data['decision']
        remarks = serializer.validated_data.get('officer_remarks', '')

        if decision == 'REJECT':
            loan.reviewed_by_officer = request.user
            loan.officer_remarks = remarks or 'Rejected by Bank Officer.'
            loan.loan_status = 'REJECTED'
            loan.save(update_fields=['reviewed_by_officer', 'officer_remarks', 'loan_status'])
        else:
            ip_addr = request.META.get('REMOTE_ADDR', '127.0.0.1')
            disburse_loan_and_generate_schedule(loan, request.user, remarks, ip_addr)

        return Response(LoanApplicationSerializer(loan).data, status=status.HTTP_200_OK)


class LoanRepaymentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, loan_id):
        loan = get_object_or_404(LoanApplication, loan_id=loan_id)
        if request.user.role.role_code not in ('ADMIN', 'BANK_OFFICER', 'AUDITOR') and loan.user_id != request.user.user_id:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        repayments = loan.repayments.all()
        return Response(LoanRepaymentSerializer(repayments, many=True).data, status=status.HTTP_200_OK)


class PayLoanEMIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, repayment_id):
        repayment = get_object_or_404(
            LoanRepayment.objects.select_related('loan', 'loan__disbursement_account'),
            repayment_id=repayment_id,
        )
        loan = repayment.loan
        if loan.user_id != request.user.user_id:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        if repayment.repayment_status == 'PAID':
            return Response({'detail': 'EMI already paid.'}, status=status.HTTP_400_BAD_REQUEST)

        total_due = repayment.emi_amount + repayment.penalty_amount
        with db_tx.atomic():
            acc = BankAccount.objects.select_for_update().get(account_id=loan.disbursement_account_id)
            if acc.balance < total_due:
                return Response({'detail': 'Insufficient balance for EMI payment.'}, status=status.HTTP_400_BAD_REQUEST)

            acc.balance -= total_due
            acc.save(update_fields=['balance', 'updated_at'])

            tx = Transaction.objects.create(
                account=acc,
                reference_utr=f'BNKEMI{timezone.now().strftime("%Y%m%d")}{uuid.uuid4().hex[:7].upper()}',
                transaction_type='DEBIT',
                channel='LOAN_EMI',
                amount=total_due,
                balance_after=acc.balance,
                description=f'Loan EMI #{repayment.installment_number} for {loan.application_number}',
                status='SUCCESS',
                initiated_ip=request.META.get('REMOTE_ADDR', '127.0.0.1'),
            )

            repayment.transaction = tx
            repayment.repayment_status = 'PAID'
            repayment.paid_at = timezone.now()
            repayment.save(update_fields=['transaction', 'repayment_status', 'paid_at'])

            loan.outstanding_principal = max(Decimal('0.00'), loan.outstanding_principal - repayment.principal_component)
            if loan.outstanding_principal == Decimal('0.00'):
                loan.loan_status = 'CLOSED'
            loan.save(update_fields=['outstanding_principal', 'loan_status'])

        return Response(
            {'message': 'EMI paid successfully.', 'repayment': LoanRepaymentSerializer(repayment).data},
            status=status.HTTP_200_OK,
        )
