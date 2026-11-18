import uuid
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction as db_tx
from django.utils import timezone
from rest_framework import serializers

from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Transaction
from .models import Investment, InvestmentPlan


class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = [
            'plan_id',
            'plan_code',
            'plan_name',
            'investment_type',
            'min_investment',
            'expected_return_rate',
            'lock_in_months',
            'premature_penalty_pct',
            'risk_level',
        ]


class InvestmentSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.plan_name', read_only=True)
    investment_type = serializers.CharField(source='plan.investment_type', read_only=True)
    account_number = serializers.CharField(source='funding_account.account_number', read_only=True)

    class Meta:
        model = Investment
        fields = [
            'investment_id',
            'certificate_number',
            'plan',
            'plan_name',
            'investment_type',
            'funding_account',
            'account_number',
            'principal_amount',
            'monthly_installment',
            'interest_rate',
            'tenure_months',
            'projected_maturity_amount',
            'start_date',
            'maturity_date',
            'auto_renew',
            'investment_status',
            'created_at',
        ]
        read_only_fields = fields


class CreateInvestmentSerializer(serializers.Serializer):
    funding_account_id = serializers.IntegerField()
    plan_id = serializers.IntegerField()
    principal_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    tenure_months = serializers.IntegerField(min_value=1, max_value=360)
    auto_renew = serializers.BooleanField(default=False)

    def validate(self, attrs):
        user = self.context['request'].user
        acc = BankAccount.objects.filter(
            account_id=attrs['funding_account_id'], user=user, account_status='ACTIVE'
        ).first()
        if not acc:
            raise serializers.ValidationError({'funding_account_id': 'Active funding account not found.'})

        plan = InvestmentPlan.objects.filter(plan_id=attrs['plan_id'], is_active=True).first()
        if not plan:
            raise serializers.ValidationError({'plan_id': 'Investment plan not found.'})

        amt = attrs['principal_amount']
        if amt < plan.min_investment:
            raise serializers.ValidationError(
                {'principal_amount': f'Minimum investment for this plan is ₹{plan.min_investment}.'}
            )
        if acc.balance < amt:
            raise serializers.ValidationError({'principal_amount': 'Insufficient account balance.'})

        attrs['account'] = acc
        attrs['plan'] = plan
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        plan = validated_data['plan']
        amt = validated_data['principal_amount']
        tenure = validated_data['tenure_months']
        acc_id = validated_data['account'].account_id

        years = Decimal(tenure) / Decimal('12')
        projected = (amt * (Decimal('1') + (plan.expected_return_rate / Decimal('100')) * years)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        start_d = timezone.localdate()
        mat_d = start_d + timedelta(days=30 * tenure)

        with db_tx.atomic():
            acc = BankAccount.objects.select_for_update().get(account_id=acc_id)
            if acc.balance < amt:
                raise serializers.ValidationError({'principal_amount': 'Insufficient balance.'})

            acc.balance -= amt
            acc.save(update_fields=['balance', 'updated_at'])

            cert_no = f'BNKINV{uuid.uuid4().hex[:8].upper()}'
            Transaction.objects.create(
                account=acc,
                reference_utr=f'BNKIV{timezone.now().strftime("%Y%m%d")}{uuid.uuid4().hex[:8].upper()}',
                transaction_type='DEBIT',
                channel='INVESTMENT',
                amount=amt,
                balance_after=acc.balance,
                description=f'Investment Booking {cert_no}',
                remarks=plan.plan_name,
                status='SUCCESS',
                initiated_ip=request.META.get('REMOTE_ADDR', '127.0.0.1'),
            )

            return Investment.objects.create(
                certificate_number=cert_no,
                user=user,
                funding_account=acc,
                plan=plan,
                principal_amount=amt,
                interest_rate=plan.expected_return_rate,
                tenure_months=tenure,
                projected_maturity_amount=projected,
                start_date=start_d,
                maturity_date=mat_d,
                auto_renew=validated_data['auto_renew'],
                investment_status='ACTIVE',
            )
