from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts_auth.views import IsBankOfficerOrAdmin
from apps.transfers.models import Transaction
from apps.transfers.serializers import TransactionSerializer
from .models import KYCDocument, SecurityAuditLog
from .serializers import KYCDocumentSerializer, SecurityAuditLogSerializer


class IsComplianceViewer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role.role_code in ('ADMIN', 'BANK_OFFICER', 'AUDITOR')
        )


class KYCDocumentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role.role_code in ('ADMIN', 'BANK_OFFICER', 'AUDITOR'):
            qs = KYCDocument.objects.select_related('user').all()
        else:
            qs = KYCDocument.objects.select_related('user').filter(user=request.user)
        return Response(KYCDocumentSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = KYCDocumentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        doc = serializer.save()
        return Response(KYCDocumentSerializer(doc).data, status=status.HTTP_201_CREATED)


class KYCVerifyView(APIView):
    permission_classes = [IsBankOfficerOrAdmin]

    def patch(self, request, kyc_doc_id):
        doc = get_object_or_404(KYCDocument, kyc_doc_id=kyc_doc_id)
        new_status = request.data.get('verification_status')
        if new_status not in ('VERIFIED', 'REJECTED'):
            return Response({'detail': 'Provide VERIFIED or REJECTED.'}, status=status.HTTP_400_BAD_REQUEST)

        doc.verification_status = new_status
        doc.verified_by_officer = request.user
        doc.verified_at = timezone.now()
        doc.rejection_reason = request.data.get('rejection_reason') if new_status == 'REJECTED' else None
        doc.save()

        doc.user.kyc_status = new_status
        doc.user.save(update_fields=['kyc_status'])

        SecurityAuditLog.objects.create(
            user=request.user,
            event_category='KYC_REVIEW',
            severity='INFO' if new_status == 'VERIFIED' else 'WARNING',
            ip_address=request.META.get('REMOTE_ADDR', '127.0.0.1'),
            user_agent=request.META.get('HTTP_USER_AGENT', 'BankEase-API')[:255],
            resource_target=f'/api/v1/security/kyc/{kyc_doc_id}/verify/',
            event_description=f'KYC document #{kyc_doc_id} marked {new_status} for {doc.user.username}',
            is_suspicious=False,
        )

        return Response(KYCDocumentSerializer(doc).data, status=status.HTTP_200_OK)


class SecurityAuditLogListView(APIView):
    permission_classes = [IsComplianceViewer]

    def get(self, request):
        qs = SecurityAuditLog.objects.select_related('user').all()[:100]
        if request.query_params.get('suspicious') == 'true':
            qs = SecurityAuditLog.objects.select_related('user').filter(is_suspicious=True)[:100]
        return Response(SecurityAuditLogSerializer(qs, many=True).data, status=status.HTTP_200_OK)


class FlaggedTransactionsView(APIView):
    permission_classes = [IsComplianceViewer]

    def get(self, request):
        qs = Transaction.objects.select_related('account', 'beneficiary').filter(is_flagged=True)
        return Response(TransactionSerializer(qs, many=True).data, status=status.HTTP_200_OK)
