from django.contrib import admin
from django.urls import include, path
from apps.accounts_auth.views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/v1/auth/', include('apps.accounts_auth.urls')),
    path('api/v1/accounts/', include('apps.banking_accounts.urls')),
    path('api/v1/transfers/', include('apps.transfers.urls')),
    path('api/v1/bills/', include('apps.bills.urls')),
    path('api/v1/loans/', include('apps.loans.urls')),
    path('api/v1/investments/', include('apps.investments.urls')),
]
