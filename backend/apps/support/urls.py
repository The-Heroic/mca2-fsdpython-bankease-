from django.urls import path
from .views import (
    SupportTicketListCreateView,
    TicketMessageListCreateView,
    TicketStatusUpdateView,
)

urlpatterns = [
    path('tickets/', SupportTicketListCreateView.as_view(), name='support-ticket-list-create'),
    path('tickets/<int:ticket_id>/messages/', TicketMessageListCreateView.as_view(), name='support-ticket-messages'),
    path('tickets/<int:ticket_id>/status/', TicketStatusUpdateView.as_view(), name='support-ticket-status'),
]
