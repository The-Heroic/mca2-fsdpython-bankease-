from django.db import models
from apps.accounts_auth.models import User


class Notification(models.Model):
    TYPES = [
        ('TRANSACTION', 'Transaction'),
        ('SECURITY', 'Security'),
        ('BILL_REMINDER', 'Bill Reminder'),
        ('LOAN_ALERT', 'Loan Alert'),
        ('INVESTMENT_UPDATE', 'Investment Update'),
        ('SUPPORT_UPDATE', 'Support Update'),
    ]
    PRIORITIES = [('NORMAL', 'Normal'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]
    CHANNELS = [('IN_APP', 'In-App'), ('EMAIL', 'Email'), ('SMS', 'SMS')]

    notification_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITIES, default='NORMAL')
    title = models.CharField(max_length=140)
    message = models.CharField(max_length=255)
    channel = models.CharField(max_length=10, choices=CHANNELS, default='IN_APP')
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at', '-notification_id']

    def __str__(self):
        return f'{self.user.username} - {self.title}'
