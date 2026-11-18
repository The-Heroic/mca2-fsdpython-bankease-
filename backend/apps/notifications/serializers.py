from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'notification_id',
            'notification_type',
            'priority',
            'title',
            'message',
            'channel',
            'is_read',
            'read_at',
            'created_at',
        ]
        read_only_fields = ['notification_id', 'is_read', 'read_at', 'created_at']

    def create(self, validated_data):
        return Notification.objects.create(user=self.context['request'].user, **validated_data)
