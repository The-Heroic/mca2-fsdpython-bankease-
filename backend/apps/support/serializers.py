import uuid
from rest_framework import serializers
from .models import SupportTicket, TicketMessage


class TicketMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender_user.full_name', read_only=True)
    sender_role = serializers.CharField(source='sender_user.role.role_code', read_only=True)

    class Meta:
        model = TicketMessage
        fields = [
            'message_id',
            'ticket',
            'sender_user',
            'sender_name',
            'sender_role',
            'message_body',
            'is_internal_note',
            'created_at',
        ]
        read_only_fields = ['message_id', 'ticket', 'sender_user', 'created_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            'ticket_id',
            'ticket_number',
            'user',
            'customer_name',
            'category',
            'priority',
            'subject',
            'description',
            'ticket_status',
            'resolution_notes',
            'created_at',
            'resolved_at',
        ]
        read_only_fields = [
            'ticket_id',
            'ticket_number',
            'user',
            'ticket_status',
            'resolution_notes',
            'created_at',
            'resolved_at',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        ticket = SupportTicket.objects.create(
            ticket_number=f'TKT{uuid.uuid4().hex[:8].upper()}',
            user=user,
            **validated_data,
        )
        TicketMessage.objects.create(
            ticket=ticket,
            sender_user=user,
            message_body=validated_data['description'],
        )
        return ticket
