from django.db import models
from apps.accounts_auth.models import User


class ReportExport(models.Model):
    REPORT_TYPES = [
        ('ACCOUNT_STATEMENT', 'Account Statement'),
        ('TAX_CERTIFICATE', 'Tax Certificate'),
        ('LOAN_AMORTIZATION', 'Loan Amortization'),
        ('BRANCH_LIQUIDITY', 'Branch Liquidity'),
        ('COMPLIANCE_AUDIT', 'Compliance Audit'),
        ('PORTFOLIO_SUMMARY', 'Portfolio Summary'),
    ]
    FORMATS = [('PDF', 'PDF'), ('CSV', 'CSV'), ('XLSX', 'XLSX')]

    report_id = models.AutoField(primary_key=True)
    generated_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_exports')
    report_type = models.CharField(max_length=25, choices=REPORT_TYPES)
    file_format = models.CharField(max_length=5, choices=FORMATS, default='CSV')
    period_start = models.DateField()
    period_end = models.DateField()
    filter_summary = models.CharField(max_length=255, null=True, blank=True)
    file_path = models.CharField(max_length=255)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report_exports'
        ordering = ['-generated_at', '-report_id']
