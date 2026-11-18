from django.urls import path
from .views import (
    DashboardAnalyticsView,
    ReportExportDownloadView,
    ReportExportListCreateView,
)

urlpatterns = [
    path('dashboard/', DashboardAnalyticsView.as_view(), name='reporting-dashboard'),
    path('exports/', ReportExportListCreateView.as_view(), name='reporting-exports'),
    path('exports/<int:report_id>/download/', ReportExportDownloadView.as_view(), name='reporting-download'),
]
