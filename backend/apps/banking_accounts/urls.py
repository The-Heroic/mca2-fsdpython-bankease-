from django.urls import path
from .views import (
    AccountDetailView,
    AccountListCreateView,
    AccountStatementView,
    AccountStatusUpdateView,
)

urlpatterns = [
    path('', AccountListCreateView.as_view(), name='account-list-create'),
    path('<int:account_id>/', AccountDetailView.as_view(), name='account-detail'),
    path('<int:account_id>/status/', AccountStatusUpdateView.as_view(), name='account-status-update'),
    path('<int:account_id>/statement/', AccountStatementView.as_view(), name='account-statement'),
]
