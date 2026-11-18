from django.db import models
from apps.accounts_auth.models import User
from apps.transfers.models import Transaction


class SupportTicket(models.Model):
    CATEGORIES = [
        ('DISPUTED_TRANSACTION', 'Disputed Transaction'),
        ('ACCOUNT_ISSUE', 'Account Issue'),
        ('FUNDS_TRANSFER', 'Funds Transfer'),
        ('BILL_PAYMENT', 'Bill Payment'),
        ('LOAN_QUERY', 'Loan Query'),
        ('INVESTMENT_QUERY', 'Investment Query'),
        ('KYC_UPDATE', 'KYC Update'),
        ('TECHNICAL_ISSUE', 'Technical Issue'),
    ]
    PRIORITIES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    STATUSES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    ticket_id = models.AutoField(primary_key=True)
    ticket_number = models.CharField(max_length=25, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    assigned_officer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets'
    )
    related_transaction = models.ForeignKey(
        Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_tickets'
    )
    category = models.CharField(max_length=25, choices=CATEGORIES)
    priority = models.CharField(max_length=10, choices=PRIORITIES, default='MEDIUM')
    subject = models.CharField(max_length=160)
    description = models.TextField()
    ticket_status = models.CharField(max_length=15, choices=STATUSES, default='OPEN', db_index=True)
    resolution_notes = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'support_tickets'
        ordering = ['-created_at', '-ticket_id']

    def __str__(self):
        return f'{self.ticket_number} - {self.subject}'


class TicketMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='ticket_messages')
    message_body = models.TextField()
    is_internal_note = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_messages'
        ordering = ['created_at', 'message_id']
