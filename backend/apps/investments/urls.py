from django.urls import path
from .views import (
    InvestmentCloseView,
    InvestmentListCreateView,
    InvestmentPlanListView,
)

urlpatterns = [
    path('plans/', InvestmentPlanListView.as_view(), name='investment-plans'),
    path('', InvestmentListCreateView.as_view(), name='investment-list-create'),
    path('<int:investment_id>/close/', InvestmentCloseView.as_view(), name='investment-close'),
]
