from rest_framework import serializers
from .models import KYCDocument, SecurityAuditLog


class KYCDocumentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = KYCDocument
        fields = [
            'kyc_doc_id',
            'user',
            'username',
            'full_name',
            'document_type',
            'document_number_masked',
            'file_path',
            'verification_status',
            'rejection_reason',
            'uploaded_at',
            'verified_at',
        ]
        read_only_fields = [
            'kyc_doc_id',
            'user',
            'verification_status',
            'rejection_reason',
            'uploaded_at',
            'verified_at',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        doc, _ = KYCDocument.objects.update_or_create(
            user=user,
            document_type=validated_data['document_type'],
            defaults={
                'document_number_masked': validated_data['document_number_masked'],
                'file_path': validated_data['file_path'],
                'verification_status': 'PENDING',
                'rejection_reason': None,
            },
        )
        if user.kyc_status == 'PENDING':
            user.kyc_status = 'SUBMITTED'
            user.save(update_fields=['kyc_status'])
        return doc


class SecurityAuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, default=None)

    class Meta:
        model = SecurityAuditLog
        fields = [
            'audit_id',
            'user',
            'username',
            'event_category',
            'severity',
            'ip_address',
            'user_agent',
            'resource_target',
            'event_description',
            'is_suspicious',
            'created_at',
        ]
        read_only_fields = fields
