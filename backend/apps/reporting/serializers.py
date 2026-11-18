import uuid
from rest_framework import serializers
from .models import ReportExport


class ReportExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExport
        fields = [
            'report_id',
            'report_type',
            'file_format',
            'period_start',
            'period_end',
            'filter_summary',
            'file_path',
            'generated_at',
        ]
        read_only_fields = ['report_id', 'file_path', 'generated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        fmt = validated_data.get('file_format', 'CSV').lower()
        path = f'/exports/{validated_data["report_type"].lower()}_{uuid.uuid4().hex[:8]}.{fmt}'
        return ReportExport.objects.create(
            generated_by_user=user,
            file_path=path,
            **validated_data,
        )
