from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse
from apps.accounts_auth.views import HealthCheckView

def root_health_view(request):
    return JsonResponse({'status': 'ok', 'app': 'BankEase REST API', 'version': '1.0.0'})

urlpatterns = [
    path('', root_health_view, name='root-health'),
    path('health/', root_health_view, name='health-alt'),
    path('admin/', admin.site.urls),
    path('api/v1/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/v1/auth/', include('apps.accounts_auth.urls')),
    path('api/v1/accounts/', include('apps.banking_accounts.urls')),
    path('api/v1/transfers/', include('apps.transfers.urls')),
    path('api/v1/bills/', include('apps.bills.urls')),
    path('api/v1/loans/', include('apps.loans.urls')),
    path('api/v1/investments/', include('apps.investments.urls')),
    path('api/v1/support/', include('apps.support.urls')),
    path('api/v1/security/', include('apps.security_compliance.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/reports/', include('apps.reporting.urls')),
]
