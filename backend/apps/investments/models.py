from decimal import Decimal
from django.db import models
from apps.accounts_auth.models import User
from apps.banking_accounts.models import BankAccount


class InvestmentPlan(models.Model):
    INVESTMENT_TYPES = [
        ('FIXED_DEPOSIT', 'Fixed Deposit'),
        ('RECURRING_DEPOSIT', 'Recurring Deposit'),
        ('MUTUAL_FUND', 'Mutual Fund'),
        ('SOVEREIGN_GOLD_BOND', 'Sovereign Gold Bond'),
        ('PPF', 'Public Provident Fund'),
    ]
    RISK_LEVELS = [('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High')]

    plan_id = models.AutoField(primary_key=True)
    plan_code = models.CharField(max_length=30, unique=True)
    plan_name = models.CharField(max_length=100, unique=True)
    investment_type = models.CharField(max_length=25, choices=INVESTMENT_TYPES)
    min_investment = models.DecimalField(max_digits=12, decimal_places=2)
    expected_return_rate = models.DecimalField(max_digits=5, decimal_places=2)
    lock_in_months = models.IntegerField()
    premature_penalty_pct = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1.00'))
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='LOW')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'investment_plans'
        ordering = ['plan_id']

    def __str__(self):
        return f'{self.plan_name} ({self.expected_return_rate}%)'


class Investment(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('MATURED', 'Matured'),
        ('PREMATURE_CLOSED', 'Premature Closed'),
        ('CANCELLED', 'Cancelled'),
    ]

    investment_id = models.AutoField(primary_key=True)
    certificate_number = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='investments')
    funding_account = models.ForeignKey(
        BankAccount, on_delete=models.RESTRICT, related_name='investments'
    )
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.RESTRICT, related_name='subscriptions')
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    monthly_installment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_months = models.IntegerField()
    projected_maturity_amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField()
    maturity_date = models.DateField()
    auto_renew = models.BooleanField(default=False)
    investment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'investments'
        ordering = ['-created_at', '-investment_id']

    def __str__(self):
        return f'{self.certificate_number} ({self.investment_status})'
