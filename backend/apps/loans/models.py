from decimal import Decimal
from django.db import models
from apps.accounts_auth.models import User
from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Transaction


class LoanProduct(models.Model):
    CATEGORIES = [
        ('PERSONAL', 'Personal Loan'),
        ('HOME', 'Home Loan'),
        ('VEHICLE', 'Vehicle Loan'),
        ('EDUCATION', 'Education Loan'),
        ('BUSINESS', 'Business Loan'),
        ('GOLD', 'Gold Loan'),
    ]

    loan_product_id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=30, unique=True)
    product_name = models.CharField(max_length=100, unique=True)
    loan_category = models.CharField(max_length=15, choices=CATEGORIES)
    min_amount = models.DecimalField(max_digits=15, decimal_places=2)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2)
    base_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    min_tenure_months = models.IntegerField()
    max_tenure_months = models.IntegerField()
    processing_fee_pct = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1.00'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loan_products'
        ordering = ['loan_product_id']

    def __str__(self):
        return f'{self.product_name} ({self.base_interest_rate}%)'


class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('DISBURSED', 'Disbursed'),
        ('REJECTED', 'Rejected'),
        ('CLOSED', 'Closed'),
        ('DEFAULTED', 'Defaulted'),
    ]

    loan_id = models.AutoField(primary_key=True)
    application_number = models.CharField(max_length=25, unique=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='loan_applications')
    disbursement_account = models.ForeignKey(
        BankAccount, on_delete=models.RESTRICT, related_name='loan_applications'
    )
    loan_product = models.ForeignKey(
        LoanProduct, on_delete=models.RESTRICT, related_name='applications'
    )
    reviewed_by_officer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_loans'
    )
    requested_amount = models.DecimalField(max_digits=15, decimal_places=2)
    sanctioned_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_months = models.IntegerField()
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding_principal = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    applicant_annual_income = models.DecimalField(max_digits=15, decimal_places=2)
    cibil_score = models.IntegerField()
    purpose_description = models.CharField(max_length=255)
    officer_remarks = models.CharField(max_length=255, null=True, blank=True)
    loan_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='APPLIED', db_index=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    disbursed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'loan_applications'
        ordering = ['-applied_at', '-loan_id']

    def __str__(self):
        return f'{self.application_number} ({self.loan_status})'


class LoanRepayment(models.Model):
    REPAYMENT_STATUSES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('WAIVED', 'Waived'),
    ]

    repayment_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='repayments')
    transaction = models.ForeignKey(
        Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='loan_repayments'
    )
    installment_number = models.IntegerField()
    due_date = models.DateField(db_index=True)
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2)
    principal_component = models.DecimalField(max_digits=12, decimal_places=2)
    interest_component = models.DecimalField(max_digits=12, decimal_places=2)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    repayment_status = models.CharField(max_length=10, choices=REPAYMENT_STATUSES, default='PENDING')
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'loan_repayments'
        ordering = ['loan', 'installment_number']
        unique_together = [('loan', 'installment_number')]

    def __str__(self):
        return f'{self.loan.application_number} - EMI #{self.installment_number}'
