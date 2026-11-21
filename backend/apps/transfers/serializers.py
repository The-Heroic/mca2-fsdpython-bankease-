import re
import uuid
from datetime import timedelta
from decimal import Decimal
from django.db import transaction as db_tx
from django.utils import timezone
from rest_framework import serializers

from apps.banking_accounts.models import BankAccount
from .models import Beneficiary, Transaction


class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = [
            'beneficiary_id',
            'nickname',
            'beneficiary_name',
            'account_number',
            'bank_name',
            'ifsc_code',
            'transfer_type',
            'daily_limit',
            'cooling_ends_at',
            'is_verified',
            'status',
            'created_at',
        ]
        read_only_fields = ['beneficiary_id', 'cooling_ends_at', 'is_verified', 'status', 'created_at']

    def validate_ifsc_code(self, value):
        code = value.strip().upper()
        if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', code):
            raise serializers.ValidationError('Invalid IFSC format (expected 11 chars, e.g., BNKE0000001).')
        return code

    def create(self, validated_data):
        user = self.context['request'].user
        ifsc = validated_data['ifsc_code']
        transfer_type = 'INTRABANK' if ifsc.startswith('BNKE') else validated_data.get('transfer_type', 'INTERBANK')
        cooling_minutes = self.context.get('cooling_minutes', 0)
        status_val = 'COOLING' if cooling_minutes > 0 else 'ACTIVE'

        return Beneficiary.objects.create(
            user=user,
            transfer_type=transfer_type,
            cooling_ends_at=timezone.now() + timedelta(minutes=cooling_minutes),
            is_verified=(status_val == 'ACTIVE'),
            status=status_val,
            **validated_data,
        )


class TransactionSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(source='account.account_number', read_only=True)
    beneficiary_name = serializers.CharField(source='beneficiary.beneficiary_name', read_only=True, default=None)

    class Meta:
        model = Transaction
        fields = [
            'transaction_id',
            'account',
            'account_number',
            'counterparty_account',
            'beneficiary',
            'beneficiary_name',
            'reference_utr',
            'transaction_type',
            'channel',
            'amount',
            'balance_after',
            'currency',
            'description',
            'remarks',
            'status',
            'is_flagged',
            'transaction_date',
        ]
        read_only_fields = fields


class ExecuteTransferSerializer(serializers.Serializer):
    source_account_id = serializers.IntegerField()
    beneficiary_id = serializers.IntegerField()
    channel = serializers.ChoiceField(choices=['IMPS', 'NEFT', 'RTGS', 'UPI', 'INTERNAL'])
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal('1.00'))
    remarks = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context['request'].user
        is_staff_or_officer = bool(
            user.role and user.role.role_code in ('ADMIN', 'BANK_OFFICER')
        )

        if is_staff_or_officer:
            source = BankAccount.objects.filter(account_id=attrs['source_account_id']).first()
        else:
            source = BankAccount.objects.filter(account_id=attrs['source_account_id'], user=user).first()

        if not source:
            raise serializers.ValidationError({'source_account_id': 'Source account not found for your profile.'})
        if source.account_status != 'ACTIVE':
            raise serializers.ValidationError({'source_account_id': f'Source account is {source.account_status}.'})

        if is_staff_or_officer:
            beneficiary = Beneficiary.objects.filter(beneficiary_id=attrs['beneficiary_id']).first()
        else:
            beneficiary = Beneficiary.objects.filter(beneficiary_id=attrs['beneficiary_id'], user=user).first()

        if not beneficiary:
            raise serializers.ValidationError({'beneficiary_id': 'Beneficiary not found.'})
        if beneficiary.status != 'ACTIVE':
            raise serializers.ValidationError({'beneficiary_id': f'Beneficiary is currently {beneficiary.status}.'})

        amount = attrs['amount']
        if amount > source.daily_transfer_limit:
            raise serializers.ValidationError({'amount': 'Amount exceeds account daily transfer limit.'})
        if amount > beneficiary.daily_limit:
            raise serializers.ValidationError({'amount': 'Amount exceeds beneficiary daily limit.'})
        if source.balance < amount:
            raise serializers.ValidationError({'amount': 'Insufficient account balance.'})

        attrs['source_account'] = source
        attrs['beneficiary'] = beneficiary
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        source_id = validated_data['source_account'].account_id
        beneficiary = validated_data['beneficiary']
        amount = validated_data['amount']
        channel = validated_data['channel']
        remarks = validated_data.get('remarks') or f'{channel} Transfer'
        ip_addr = request.META.get('REMOTE_ADDR', '127.0.0.1')

        with db_tx.atomic():
            src = BankAccount.objects.select_for_update().get(account_id=source_id)
            if src.balance < amount:
                raise serializers.ValidationError({'amount': 'Insufficient account balance.'})

            src.balance -= amount
            src.save(update_fields=['balance', 'updated_at'])

            counterparty = None
            if beneficiary.transfer_type == 'INTRABANK':
                counterparty = BankAccount.objects.select_for_update().filter(
                    account_number=beneficiary.account_number,
                    account_status='ACTIVE',
                ).first()

            is_flagged = amount >= Decimal('500000.00')
            utr = f'BNK{timezone.now().strftime("%Y%m%d")}{uuid.uuid4().hex[:10].upper()}'

            debit_tx = Transaction.objects.create(
                account=src,
                counterparty_account=counterparty,
                beneficiary=beneficiary,
                reference_utr=utr,
                transaction_type='DEBIT',
                channel=channel,
                amount=amount,
                balance_after=src.balance,
                description=f'{channel} Transfer to {beneficiary.beneficiary_name}',
                remarks=remarks,
                status='FLAGGED' if is_flagged else 'SUCCESS',
                is_flagged=is_flagged,
                initiated_ip=ip_addr,
            )

            if counterparty and counterparty.account_id != src.account_id:
                counterparty.balance += amount
                counterparty.save(update_fields=['balance', 'updated_at'])
                Transaction.objects.create(
                    account=counterparty,
                    counterparty_account=src,
                    reference_utr=f'{utr}-CR',
                    transaction_type='CREDIT',
                    channel=channel,
                    amount=amount,
                    balance_after=counterparty.balance,
                    description=f'{channel} Credit from {src.user.full_name}',
                    remarks=remarks,
                    status='SUCCESS',
                    is_flagged=False,
                    initiated_ip=ip_addr,
                )

            return debit_tx
