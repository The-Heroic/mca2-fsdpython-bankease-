import random
from decimal import Decimal
from django.utils import timezone
from rest_framework import serializers
from apps.accounts_auth.models import Branch
from .models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='user.username', read_only=True)
    owner_name = serializers.CharField(source='user.full_name', read_only=True)
    branch_ifsc = serializers.CharField(source='branch.ifsc_code', read_only=True)
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)

    class Meta:
        model = BankAccount
        fields = [
            'account_id',
            'user',
            'owner_username',
            'owner_name',
            'branch',
            'branch_ifsc',
            'branch_name',
            'account_number',
            'account_type',
            'currency',
            'balance',
            'minimum_balance',
            'daily_transfer_limit',
            'interest_rate',
            'account_status',
            'nominee_name',
            'nominee_relation',
            'opened_at',
            'closed_at',
            'created_at',
        ]
        read_only_fields = [
            'account_id',
            'user',
            'account_number',
            'currency',
            'account_status',
            'opened_at',
            'closed_at',
            'created_at',
        ]


class OpenAccountSerializer(serializers.Serializer):
    branch_id = serializers.IntegerField(required=False)
    account_type = serializers.ChoiceField(choices=['SAVINGS', 'CURRENT', 'SALARY'], default='SAVINGS')
    initial_deposit = serializers.DecimalField(
        max_digits=15, decimal_places=2, min_value=Decimal('0.00'), default=Decimal('5000.00')
    )
    nominee_name = serializers.CharField(max_length=120, required=False, allow_blank=True)
    nominee_relation = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def create(self, validated_data):
        user = self.context['request'].user
        branch_id = validated_data.get('branch_id')
        if branch_id:
            branch = Branch.objects.filter(branch_id=branch_id).first()
            if not branch:
                raise serializers.ValidationError({'branch_id': 'Selected branch does not exist.'})
        else:
            branch = user.home_branch or Branch.objects.first()
            if not branch:
                branch = Branch.objects.create(
                    ifsc_code='BNKE0000001',
                    branch_name='Connaught Place Main Branch',
                    address_line='Block A, Connaught Place',
                    city='New Delhi',
                    state='Delhi',
                    pincode='110001',
                    contact_phone='+91-1123415001',
                )

        # Generate unique 12-digit account number
        while True:
            acc_no = f'1800{random.randint(10000000, 99999999)}'
            if not BankAccount.objects.filter(account_number=acc_no).exists():
                break

        acc_type = validated_data['account_type']
        min_bal = Decimal('25000.00') if acc_type == 'CURRENT' else (
            Decimal('0.00') if acc_type == 'SALARY' else Decimal('1000.00')
        )
        rate = Decimal('0.00') if acc_type == 'CURRENT' else Decimal('3.50')
        status_val = 'ACTIVE' if user.kyc_status == 'VERIFIED' else 'PENDING_KYC'

        return BankAccount.objects.create(
            user=user,
            branch=branch,
            account_number=acc_no,
            account_type=acc_type,
            balance=validated_data['initial_deposit'],
            minimum_balance=min_bal,
            interest_rate=rate,
            account_status=status_val,
            nominee_name=validated_data.get('nominee_name') or None,
            nominee_relation=validated_data.get('nominee_relation') or None,
            opened_at=timezone.localdate(),
        )


class UpdateAccountStatusSerializer(serializers.Serializer):
    account_status = serializers.ChoiceField(
        choices=['PENDING_KYC', 'ACTIVE', 'FROZEN', 'DORMANT', 'CLOSED']
    )
