from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Notification.objects.filter(user=request.user)[:50]
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response(
            {
                'unread_count': unread_count,
                'notifications': NotificationSerializer(qs, many=True).data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = NotificationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        notif = serializer.save()
        return Response(NotificationSerializer(notif).data, status=status.HTTP_201_CREATED)


class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, notification_id):
        notif = get_object_or_404(Notification, notification_id=notification_id, user=request.user)
        notif.is_read = True
        notif.read_at = timezone.now()
        notif.save(update_fields=['is_read', 'read_at'])
        return Response(NotificationSerializer(notif).data, status=status.HTTP_200_OK)


class MarkAllNotificationsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        updated = Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )
        return Response({'marked_read': updated}, status=status.HTTP_200_OK)
