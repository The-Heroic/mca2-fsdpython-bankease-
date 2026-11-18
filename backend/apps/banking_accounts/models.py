from decimal import Decimal
from django.db import models
from apps.accounts_auth.models import Branch, User


class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('SAVINGS', 'Savings Account'),
        ('CURRENT', 'Current Account'),
        ('SALARY', 'Salary Account'),
    ]
    ACCOUNT_STATUSES = [
        ('PENDING_KYC', 'Pending KYC'),
        ('ACTIVE', 'Active'),
        ('FROZEN', 'Frozen'),
        ('DORMANT', 'Dormant'),
        ('CLOSED', 'Closed'),
    ]

    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='bank_accounts')
    branch = models.ForeignKey(Branch, on_delete=models.RESTRICT, related_name='bank_accounts')
    account_number = models.CharField(max_length=12, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='SAVINGS', db_index=True)
    currency = models.CharField(max_length=3, default='INR')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    minimum_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))
    daily_transfer_limit = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('200000.00'))
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('3.50'))
    account_status = models.CharField(
        max_length=15, choices=ACCOUNT_STATUSES, default='ACTIVE', db_index=True
    )
    nominee_name = models.CharField(max_length=120, null=True, blank=True)
    nominee_relation = models.CharField(max_length=50, null=True, blank=True)
    opened_at = models.DateField()
    closed_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bank_accounts'
        ordering = ['account_id']

    def __str__(self):
        return f'{self.account_number} ({self.account_type} - {self.account_status})'
