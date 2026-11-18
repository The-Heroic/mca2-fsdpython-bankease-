from django.urls import path
from .views import (
    FlaggedTransactionsView,
    KYCDocumentListCreateView,
    KYCVerifyView,
    SecurityAuditLogListView,
)

urlpatterns = [
    path('kyc/', KYCDocumentListCreateView.as_view(), name='kyc-list-create'),
    path('kyc/<int:kyc_doc_id>/verify/', KYCVerifyView.as_view(), name='kyc-verify'),
    path('audit-logs/', SecurityAuditLogListView.as_view(), name='security-audit-logs'),
    path('flagged-transactions/', FlaggedTransactionsView.as_view(), name='flagged-transactions'),
]
