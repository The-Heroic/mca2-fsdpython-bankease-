from django.urls import path
from .views import (
    MarkAllNotificationsReadView,
    MarkNotificationReadView,
    NotificationListCreateView,
)

urlpatterns = [
    path('', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('mark-all-read/', MarkAllNotificationsReadView.as_view(), name='notification-mark-all-read'),
]
