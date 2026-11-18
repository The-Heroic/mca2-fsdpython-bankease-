from django.contrib import admin
from django.urls import include, path
from apps.accounts_auth.views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/v1/auth/', include('apps.accounts_auth.urls')),
]
