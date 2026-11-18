from decimal import Decimal
from django.db import models
from apps.accounts_auth.models import User
from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Transaction


class BillerDirectory(models.Model):
    CATEGORIES = [
        ('ELECTRICITY', 'Electricity'),
        ('WATER', 'Water'),
        ('PIPED_GAS', 'Piped Gas'),
        ('BROADBAND', 'Broadband'),
        ('DTH', 'DTH'),
        ('MOBILE_POSTPAID', 'Mobile Postpaid'),
        ('CREDIT_CARD', 'Credit Card'),
        ('INSURANCE', 'Insurance'),
    ]

    biller_id = models.AutoField(primary_key=True)
    biller_code = models.CharField(max_length=30, unique=True)
    biller_name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, db_index=True)
    coverage_state = models.CharField(max_length=60, default='PAN_INDIA')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'biller_directory'
        ordering = ['biller_id']

    def __str__(self):
        return f'{self.biller_name} ({self.category})'


class CustomerBiller(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('REMOVED', 'Removed'),
    ]

    customer_biller_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_billers')
    biller = models.ForeignKey(BillerDirectory, on_delete=models.RESTRICT, related_name='customer_links')
    consumer_number = models.CharField(max_length=50)
    short_name = models.CharField(max_length=60, null=True, blank=True)
    autopay_enabled = models.BooleanField(default=False)
    autopay_max_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_account = models.ForeignKey(
        BankAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_billers'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customer_billers'
        ordering = ['customer_biller_id']
        unique_together = [('user', 'biller', 'consumer_number')]

    def __str__(self):
        return f'{self.short_name or self.biller.biller_name} - {self.consumer_number}'


class BillPayment(models.Model):
    PAYMENT_MODES = [('MANUAL', 'Manual'), ('AUTOPAY', 'Autopay')]
    PAYMENT_STATUSES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('OVERDUE', 'Overdue'),
    ]

    bill_payment_id = models.AutoField(primary_key=True)
    customer_biller = models.ForeignKey(
        CustomerBiller, on_delete=models.RESTRICT, related_name='payments'
    )
    account = models.ForeignKey(BankAccount, on_delete=models.RESTRICT, related_name='bill_payments')
    transaction = models.ForeignKey(
        Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='bill_payments'
    )
    bbps_ref_no = models.CharField(max_length=35, unique=True)
    bill_period = models.CharField(max_length=30)
    bill_amount = models.DecimalField(max_digits=12, decimal_places=2)
    convenience_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    total_paid = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES, default='MANUAL')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUSES, default='PAID')
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bill_payments'
        ordering = ['-created_at', '-bill_payment_id']

    def __str__(self):
        return f'{self.bbps_ref_no} (INR {self.total_paid})'
