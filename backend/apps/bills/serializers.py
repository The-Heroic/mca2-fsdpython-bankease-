import uuid
from decimal import Decimal
from django.db import transaction as db_tx
from django.utils import timezone
from rest_framework import serializers

from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Transaction
from .models import BillerDirectory, BillPayment, CustomerBiller


class BillerDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillerDirectory
        fields = ['biller_id', 'biller_code', 'biller_name', 'category', 'coverage_state', 'is_active']


class CustomerBillerSerializer(serializers.ModelSerializer):
    biller_name = serializers.CharField(source='biller.biller_name', read_only=True)
    category = serializers.CharField(source='biller.category', read_only=True)

    class Meta:
        model = CustomerBiller
        fields = [
            'customer_biller_id',
            'biller',
            'biller_name',
            'category',
            'consumer_number',
            'short_name',
            'autopay_enabled',
            'autopay_max_limit',
            'preferred_account',
            'status',
            'created_at',
        ]
        read_only_fields = ['customer_biller_id', 'status', 'created_at']

    def create(self, validated_data):
        return CustomerBiller.objects.create(user=self.context['request'].user, **validated_data)


class BillPaymentSerializer(serializers.ModelSerializer):
    biller_name = serializers.CharField(source='customer_biller.biller.biller_name', read_only=True)
    consumer_number = serializers.CharField(source='customer_biller.consumer_number', read_only=True)
    account_number = serializers.CharField(source='account.account_number', read_only=True)

    class Meta:
        model = BillPayment
        fields = [
            'bill_payment_id',
            'customer_biller',
            'biller_name',
            'consumer_number',
            'account',
            'account_number',
            'bbps_ref_no',
            'bill_period',
            'bill_amount',
            'convenience_fee',
            'total_paid',
            'due_date',
            'payment_mode',
            'payment_status',
            'paid_at',
        ]
        read_only_fields = fields


class ExecuteBillPaySerializer(serializers.Serializer):
    customer_biller_id = serializers.IntegerField()
    account_id = serializers.IntegerField()
    bill_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('1.00'))
    bill_period = serializers.CharField(max_length=30, default='Nov-2026')
    payment_mode = serializers.ChoiceField(choices=['MANUAL', 'AUTOPAY'], default='MANUAL')

    def validate(self, attrs):
        user = self.context['request'].user
        cb = CustomerBiller.objects.select_related('biller').filter(
            customer_biller_id=attrs['customer_biller_id'], user=user, status='ACTIVE'
        ).first()
        if not cb:
            raise serializers.ValidationError({'customer_biller_id': 'Active registered biller not found.'})

        acc = BankAccount.objects.filter(account_id=attrs['account_id'], user=user).first()
        if not acc:
            raise serializers.ValidationError({'account_id': 'Source account not found.'})
        if acc.account_status != 'ACTIVE':
            raise serializers.ValidationError({'account_id': f'Source account is {acc.account_status}.'})

        fee = Decimal('0.00') if attrs['payment_mode'] == 'AUTOPAY' else Decimal('5.00')
        total = attrs['bill_amount'] + fee
        if acc.balance < total:
            raise serializers.ValidationError({'bill_amount': 'Insufficient balance to pay bill + fee.'})

        attrs['customer_biller'] = cb
        attrs['account'] = acc
        attrs['fee'] = fee
        attrs['total'] = total
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        cb = validated_data['customer_biller']
        acc_id = validated_data['account'].account_id
        total = validated_data['total']
        fee = validated_data['fee']
        bill_amount = validated_data['bill_amount']

        with db_tx.atomic():
            acc = BankAccount.objects.select_for_update().get(account_id=acc_id)
            if acc.balance < total:
                raise serializers.ValidationError({'bill_amount': 'Insufficient balance.'})

            acc.balance -= total
            acc.save(update_fields=['balance', 'updated_at'])

            utr = f'BNKBP{timezone.now().strftime("%Y%m%d")}{uuid.uuid4().hex[:8].upper()}'
            tx = Transaction.objects.create(
                account=acc,
                reference_utr=utr,
                transaction_type='DEBIT',
                channel='BILL_PAY',
                amount=total,
                balance_after=acc.balance,
                description=f'Bill Pay: {cb.biller.biller_name} ({cb.consumer_number})',
                remarks=validated_data['bill_period'],
                status='SUCCESS',
                initiated_ip=request.META.get('REMOTE_ADDR', '127.0.0.1'),
            )

            return BillPayment.objects.create(
                customer_biller=cb,
                account=acc,
                transaction=tx,
                bbps_ref_no=f'BBPS{uuid.uuid4().hex[:12].upper()}',
                bill_period=validated_data['bill_period'],
                bill_amount=bill_amount,
                convenience_fee=fee,
                total_paid=total,
                due_date=timezone.localdate(),
                payment_mode=validated_data['payment_mode'],
                payment_status='PAID',
                paid_at=timezone.now(),
            )
