from django.db import models
from apps.accounts_auth.models import User


class KYCDocument(models.Model):
    DOC_TYPES = [
        ('PAN_CARD', 'PAN Card'),
        ('AADHAAR_CARD', 'Aadhaar Card'),
        ('PASSPORT', 'Passport'),
        ('DRIVING_LICENSE', 'Driving License'),
        ('VOTER_ID', 'Voter ID'),
        ('SALARY_SLIP', 'Salary Slip'),
    ]
    VERIFICATION_STATUSES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    kyc_doc_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    verified_by_officer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_kyc_docs'
    )
    document_type = models.CharField(max_length=20, choices=DOC_TYPES)
    document_number_masked = models.CharField(max_length=30)
    file_path = models.CharField(max_length=255)
    verification_status = models.CharField(
        max_length=12, choices=VERIFICATION_STATUSES, default='PENDING', db_index=True
    )
    rejection_reason = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'kyc_documents'
        ordering = ['-uploaded_at', '-kyc_doc_id']
        unique_together = [('user', 'document_type')]

    def __str__(self):
        return f'{self.user.username} - {self.document_type} ({self.verification_status})'


class SecurityAuditLog(models.Model):
    CATEGORIES = [
        ('AUTH_LOGIN', 'Auth Login'),
        ('AUTH_FAILED', 'Auth Failed'),
        ('ACCOUNT_LOCK', 'Account Lock'),
        ('PASSWORD_CHANGE', 'Password Change'),
        ('HIGH_VALUE_TX', 'High Value Transaction'),
        ('KYC_REVIEW', 'KYC Review'),
        ('ACCOUNT_STATUS_CHANGE', 'Account Status Change'),
        ('ROLE_CHANGE', 'Role Change'),
        ('DATA_EXPORT', 'Data Export'),
    ]
    SEVERITIES = [('INFO', 'Info'), ('WARNING', 'Warning'), ('CRITICAL', 'Critical')]

    audit_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    event_category = models.CharField(max_length=25, choices=CATEGORIES)
    severity = models.CharField(max_length=10, choices=SEVERITIES, default='INFO')
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=255)
    resource_target = models.CharField(max_length=100, null=True, blank=True)
    event_description = models.CharField(max_length=255)
    is_suspicious = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'security_audit_logs'
        ordering = ['-created_at', '-audit_id']
