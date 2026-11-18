import csv
from decimal import Decimal
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.banking_accounts.models import BankAccount
from apps.investments.models import Investment
from apps.loans.models import LoanApplication
from apps.notifications.models import Notification
from apps.support.models import SupportTicket
from apps.transfers.models import Transaction
from apps.transfers.serializers import TransactionSerializer
from .models import ReportExport
from .serializers import ReportExportSerializer


class DashboardAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.role.role_code
        unread_alerts = Notification.objects.filter(user=user, is_read=False).count()

        if role in ('ADMIN', 'BANK_OFFICER', 'AUDITOR'):
            total_deposits = BankAccount.objects.aggregate(total=Sum('balance'))['total'] or Decimal('0.00')
            active_accounts = BankAccount.objects.filter(account_status='ACTIVE').count()
            pending_kyc_accounts = BankAccount.objects.filter(account_status='PENDING_KYC').count()
            pending_loans = LoanApplication.objects.filter(loan_status='APPLIED').count()
            open_tickets = SupportTicket.objects.filter(ticket_status__in=['OPEN', 'IN_PROGRESS']).count()
            flagged_tx = Transaction.objects.filter(is_flagged=True).count()
            recent_tx = Transaction.objects.select_related('account', 'beneficiary').all()[:10]

            return Response(
                {
                    'role': role,
                    'kpis': {
                        'total_bank_deposits': str(total_deposits),
                        'active_accounts': active_accounts,
                        'pending_kyc_accounts': pending_kyc_accounts,
                        'pending_loan_applications': pending_loans,
                        'open_support_tickets': open_tickets,
                        'flagged_transactions': flagged_tx,
                        'unread_notifications': unread_alerts,
                    },
                    'recent_transactions': TransactionSerializer(recent_tx, many=True).data,
                },
                status=status.HTTP_200_OK,
            )

        # Customer Dashboard
        total_balance = BankAccount.objects.filter(user=user).aggregate(total=Sum('balance'))['total'] or Decimal('0.00')
        account_count = BankAccount.objects.filter(user=user).count()
        active_loans = LoanApplication.objects.filter(user=user, loan_status='DISBURSED').count()
        total_investments = Investment.objects.filter(user=user, investment_status='ACTIVE').aggregate(
            total=Sum('principal_amount')
        )['total'] or Decimal('0.00')
        monthly_credits = Transaction.objects.filter(account__user=user, transaction_type='CREDIT').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        monthly_debits = Transaction.objects.filter(account__user=user, transaction_type='DEBIT').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        recent_tx = Transaction.objects.select_related('account', 'beneficiary').filter(account__user=user)[:10]

        return Response(
            {
                'role': role,
                'kpis': {
                    'total_balance': str(total_balance),
                    'account_count': account_count,
                    'active_loans': active_loans,
                    'total_investments': str(total_investments),
                    'total_credits': str(monthly_credits),
                    'total_debits': str(monthly_debits),
                    'unread_notifications': unread_alerts,
                },
                'recent_transactions': TransactionSerializer(recent_tx, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


class ReportExportListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = ReportExport.objects.filter(generated_by_user=request.user)
        return Response(ReportExportSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReportExportSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        rep = serializer.save()
        return Response(ReportExportSerializer(rep).data, status=status.HTTP_201_CREATED)


class ReportExportDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, report_id):
        rep = get_object_or_404(ReportExport, report_id=report_id, generated_by_user=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="bankease_report_{rep.report_id}.csv"'

        writer = csv.writer(response)
        writer.writerow(['UTR', 'Account', 'Type', 'Channel', 'Amount (INR)', 'Balance After', 'Status', 'Date'])
        txs = Transaction.objects.select_related('account').filter(
            account__user=request.user,
            transaction_date__date__gte=rep.period_start,
            transaction_date__date__lte=rep.period_end,
        )
        for tx in txs:
            writer.writerow([
                tx.reference_utr,
                tx.account.account_number,
                tx.transaction_type,
                tx.channel,
                tx.amount,
                tx.balance_after,
                tx.status,
                tx.transaction_date.isoformat(),
            ])
        return response
