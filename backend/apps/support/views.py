from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SupportTicket, TicketMessage
from .serializers import SupportTicketSerializer, TicketMessageSerializer


class SupportTicketListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role.role_code in ('ADMIN', 'BANK_OFFICER'):
            qs = SupportTicket.objects.select_related('user').all()
        else:
            qs = SupportTicket.objects.select_related('user').filter(user=request.user)
        return Response(SupportTicketSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SupportTicketSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        return Response(SupportTicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


class TicketMessageListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def _get_ticket(self, request, ticket_id):
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        if request.user.role.role_code not in ('ADMIN', 'BANK_OFFICER') and ticket.user_id != request.user.user_id:
            return None
        return ticket

    def get(self, request, ticket_id):
        ticket = self._get_ticket(request, ticket_id)
        if not ticket:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        msgs = ticket.messages.select_related('sender_user', 'sender_user__role').all()
        return Response(TicketMessageSerializer(msgs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, ticket_id):
        ticket = self._get_ticket(request, ticket_id)
        if not ticket:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        body = (request.data.get('message_body') or '').strip()
        if not body:
            return Response({'detail': 'Message body is required.'}, status=status.HTTP_400_BAD_REQUEST)

        msg = TicketMessage.objects.create(
            ticket=ticket,
            sender_user=request.user,
            message_body=body,
        )
        if request.user.role.role_code in ('ADMIN', 'BANK_OFFICER') and ticket.ticket_status == 'OPEN':
            ticket.ticket_status = 'IN_PROGRESS'
            ticket.assigned_officer = request.user
            ticket.save(update_fields=['ticket_status', 'assigned_officer'])

        return Response(TicketMessageSerializer(msg).data, status=status.HTTP_201_CREATED)


class TicketStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, ticket_id):
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        is_officer = request.user.role.role_code in ('ADMIN', 'BANK_OFFICER')
        if not is_officer and ticket.user_id != request.user.user_id:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('ticket_status')
        if new_status not in ('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'):
            return Response({'detail': 'Invalid ticket status.'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.ticket_status = new_status
        if new_status in ('RESOLVED', 'CLOSED'):
            ticket.resolved_at = timezone.now()
            if request.data.get('resolution_notes'):
                ticket.resolution_notes = request.data['resolution_notes']
        if is_officer and not ticket.assigned_officer:
            ticket.assigned_officer = request.user

        ticket.save()
        return Response(SupportTicketSerializer(ticket).data, status=status.HTTP_200_OK)
