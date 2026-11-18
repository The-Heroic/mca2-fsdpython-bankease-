import uuid
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction as db_tx
from django.utils import timezone
from rest_framework import serializers

from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Transaction
from .models import LoanApplication, LoanProduct, LoanRepayment


def compute_emi(principal: Decimal, annual_rate_pct: Decimal, tenure_months: int) -> Decimal:
    if annual_rate_pct <= 0:
        return (principal / tenure_months).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    r = (annual_rate_pct / Decimal('1200'))
    factor = (Decimal('1') + r) ** tenure_months
    emi = principal * r * factor / (factor - Decimal('1'))
    return emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class LoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProduct
        fields = [
            'loan_product_id',
            'product_code',
            'product_name',
            'loan_category',
            'min_amount',
            'max_amount',
            'base_interest_rate',
            'min_tenure_months',
            'max_tenure_months',
            'processing_fee_pct',
        ]


class LoanApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='user.full_name', read_only=True)
    product_name = serializers.CharField(source='loan_product.product_name', read_only=True)
    account_number = serializers.CharField(source='disbursement_account.account_number', read_only=True)

    class Meta:
        model = LoanApplication
        fields = [
            'loan_id',
            'application_number',
            'user',
            'applicant_name',
            'disbursement_account',
            'account_number',
            'loan_product',
            'product_name',
            'requested_amount',
            'sanctioned_amount',
            'interest_rate',
            'tenure_months',
            'emi_amount',
            'outstanding_principal',
            'applicant_annual_income',
            'cibil_score',
            'purpose_description',
            'officer_remarks',
            'loan_status',
            'applied_at',
            'approved_at',
            'disbursed_at',
        ]
        read_only_fields = fields


class ApplyLoanSerializer(serializers.Serializer):
    disbursement_account_id = serializers.IntegerField()
    loan_product_id = serializers.IntegerField()
    requested_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    tenure_months = serializers.IntegerField(min_value=1)
    applicant_annual_income = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal('10000.00'))
    cibil_score = serializers.IntegerField(min_value=300, max_value=900)
    purpose_description = serializers.CharField(max_length=255)

    def validate(self, attrs):
        user = self.context['request'].user
        acc = BankAccount.objects.filter(
            account_id=attrs['disbursement_account_id'], user=user, account_status='ACTIVE'
        ).first()
        if not acc:
            raise serializers.ValidationError({'disbursement_account_id': 'Active disbursement account not found.'})

        product = LoanProduct.objects.filter(
            loan_product_id=attrs['loan_product_id'], is_active=True
        ).first()
        if not product:
            raise serializers.ValidationError({'loan_product_id': 'Loan product not found.'})

        amt = attrs['requested_amount']
        if amt < product.min_amount or amt > product.max_amount:
            raise serializers.ValidationError(
                {'requested_amount': f'Amount must be between ₹{product.min_amount} and ₹{product.max_amount}.'}
            )
        tenure = attrs['tenure_months']
        if tenure < product.min_tenure_months or tenure > product.max_tenure_months:
            raise serializers.ValidationError(
                {'tenure_months': f'Tenure must be between {product.min_tenure_months} and {product.max_tenure_months} months.'}
            )

        attrs['account'] = acc
        attrs['product'] = product
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        amt = validated_data['requested_amount']
        tenure = validated_data['tenure_months']
        emi = compute_emi(amt, product.base_interest_rate, tenure)

        return LoanApplication.objects.create(
            application_number=f'BNKLN{uuid.uuid4().hex[:9].upper()}',
            user=user,
            disbursement_account=validated_data['account'],
            loan_product=product,
            requested_amount=amt,
            interest_rate=product.base_interest_rate,
            tenure_months=tenure,
            emi_amount=emi,
            applicant_annual_income=validated_data['applicant_annual_income'],
            cibil_score=validated_data['cibil_score'],
            purpose_description=validated_data['purpose_description'],
            loan_status='APPLIED',
        )


class ReviewLoanSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=['APPROVE_AND_DISBURSE', 'REJECT'])
    officer_remarks = serializers.CharField(max_length=255, required=False, allow_blank=True)


class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = [
            'repayment_id',
            'loan',
            'installment_number',
            'due_date',
            'emi_amount',
            'principal_component',
            'interest_component',
            'penalty_amount',
            'repayment_status',
            'paid_at',
        ]
        read_only_fields = fields


def disburse_loan_and_generate_schedule(loan: LoanApplication, officer, remarks: str, ip_addr: str):
    with db_tx.atomic():
        acc = BankAccount.objects.select_for_update().get(account_id=loan.disbursement_account_id)
        sanctioned = loan.requested_amount
        acc.balance += sanctioned
        acc.save(update_fields=['balance', 'updated_at'])

        now = timezone.now()
        loan.reviewed_by_officer = officer
        loan.sanctioned_amount = sanctioned
        loan.outstanding_principal = sanctioned
        loan.officer_remarks = remarks or 'Approved and disbursed by Bank Officer.'
        loan.loan_status = 'DISBURSED'
        loan.approved_at = now
        loan.disbursed_at = now
        loan.save()

        Transaction.objects.create(
            account=acc,
            reference_utr=f'BNKLN{now.strftime("%Y%m%d")}{uuid.uuid4().hex[:8].upper()}',
            transaction_type='CREDIT',
            channel='LOAN_DISBURSAL',
            amount=sanctioned,
            balance_after=acc.balance,
            description=f'Loan Disbursal {loan.application_number}',
            remarks=loan.loan_product.product_name,
            status='SUCCESS',
            initiated_ip=ip_addr,
        )

        # Generate EMI amortization schedule (capped at 12 preview installments or full tenure if <= 24)
        remaining = sanctioned
        monthly_rate = loan.interest_rate / Decimal('1200')
        base_due = timezone.localdate()
        repayments = []
        for inst in range(1, loan.tenure_months + 1):
            interest_comp = (remaining * monthly_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            principal_comp = (loan.emi_amount - interest_comp).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            if inst == loan.tenure_months or principal_comp > remaining:
                principal_comp = remaining
            remaining = max(Decimal('0.00'), remaining - principal_comp)
            repayments.append(
                LoanRepayment(
                    loan=loan,
                    installment_number=inst,
                    due_date=base_due + timedelta(days=30 * inst),
                    emi_amount=loan.emi_amount,
                    principal_component=principal_comp,
                    interest_component=interest_comp,
                    repayment_status='PENDING',
                )
            )
        LoanRepayment.objects.bulk_create(repayments)
