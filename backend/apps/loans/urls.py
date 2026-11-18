from django.urls import path
from .views import (
    EMICalculatorView,
    LoanApplicationListCreateView,
    LoanProductListView,
    LoanRepaymentListView,
    LoanReviewView,
    PayLoanEMIView,
)

urlpatterns = [
    path('products/', LoanProductListView.as_view(), name='loan-products'),
    path('calculate-emi/', EMICalculatorView.as_view(), name='loan-calculate-emi'),
    path('applications/', LoanApplicationListCreateView.as_view(), name='loan-application-list-create'),
    path('applications/<int:loan_id>/review/', LoanReviewView.as_view(), name='loan-review'),
    path('applications/<int:loan_id>/repayments/', LoanRepaymentListView.as_view(), name='loan-repayments'),
    path('repayments/<int:repayment_id>/pay/', PayLoanEMIView.as_view(), name='loan-pay-emi'),
]
