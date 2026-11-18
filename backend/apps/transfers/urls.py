from django.urls import path
from .views import (
    BeneficiaryActivateView,
    BeneficiaryListCreateView,
    ExecuteTransferView,
    TransferHistoryView,
)

urlpatterns = [
    path('beneficiaries/', BeneficiaryListCreateView.as_view(), name='beneficiary-list-create'),
    path('beneficiaries/<int:beneficiary_id>/activate/', BeneficiaryActivateView.as_view(), name='beneficiary-activate'),
    path('execute/', ExecuteTransferView.as_view(), name='transfer-execute'),
    path('history/', TransferHistoryView.as_view(), name='transfer-history'),
]
