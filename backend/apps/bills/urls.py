from django.urls import path
from .views import (
    BillerDirectoryListView,
    BillPaymentHistoryView,
    CustomerBillerListCreateView,
    ExecuteBillPayView,
)

urlpatterns = [
    path('directory/', BillerDirectoryListView.as_view(), name='biller-directory'),
    path('my-billers/', CustomerBillerListCreateView.as_view(), name='customer-biller-list-create'),
    path('pay/', ExecuteBillPayView.as_view(), name='bill-pay-execute'),
    path('history/', BillPaymentHistoryView.as_view(), name='bill-pay-history'),
]
