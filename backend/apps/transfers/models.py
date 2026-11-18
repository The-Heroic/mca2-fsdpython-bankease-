from decimal import Decimal
from django.db import models
from apps.accounts_auth.models import User
from apps.banking_accounts.models import BankAccount


class Beneficiary(models.Model):
    TRANSFER_TYPES = [
        ('INTRABANK', 'Intra-bank'),
        ('INTERBANK', 'Inter-bank'),
    ]
    STATUS_CHOICES = [
        ('COOLING', 'Cooling'),
        ('ACTIVE', 'Active'),
        ('BLOCKED', 'Blocked'),
    ]

    beneficiary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beneficiaries')
    nickname = models.CharField(max_length=60, null=True, blank=True)
    beneficiary_name = models.CharField(max_length=120)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=11)
    transfer_type = models.CharField(max_length=10, choices=TRANSFER_TYPES, default='INTERBANK')
    daily_limit = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('100000.00'))
    cooling_ends_at = models.DateTimeField()
    is_verified = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'beneficiaries'
        ordering = ['beneficiary_id']
        unique_together = [('user', 'account_number', 'ifsc_code')]

    def __str__(self):
        return f'{self.beneficiary_name} ({self.ifsc_code})'


class Transaction(models.Model):
    TX_TYPES = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]
    CHANNELS = [
        ('IMPS', 'IMPS'),
        ('NEFT', 'NEFT'),
        ('RTGS', 'RTGS'),
        ('UPI', 'UPI'),
        ('INTERNAL', 'Internal'),
        ('BILL_PAY', 'Bill Payment'),
        ('LOAN_DISBURSAL', 'Loan Disbursal'),
        ('LOAN_EMI', 'Loan EMI'),
        ('INVESTMENT', 'Investment'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REVERSED', 'Reversed'),
        ('FLAGGED', 'Flagged'),
    ]

    transaction_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(BankAccount, on_delete=models.RESTRICT, related_name='transactions')
    counterparty_account = models.ForeignKey(
        BankAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='counterparty_transactions'
    )
    beneficiary = models.ForeignKey(
        Beneficiary, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions'
    )
    reference_utr = models.CharField(max_length=30, unique=True)
    transaction_type = models.CharField(max_length=6, choices=TX_TYPES)
    channel = models.CharField(max_length=15, choices=CHANNELS)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    description = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SUCCESS')
    is_flagged = models.BooleanField(default=False, db_index=True)
    initiated_ip = models.CharField(max_length=45, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-transaction_date', '-transaction_id']

    def __str__(self):
        return f'{self.reference_utr} - {self.transaction_type} INR {self.amount}'
