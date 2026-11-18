from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    BranchListView,
    ChangePasswordView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
    UnlockUserView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('me/', ProfileView.as_view(), name='auth-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
    path('branches/', BranchListView.as_view(), name='auth-branches'),
    path('unlock-user/<int:user_id>/', UnlockUserView.as_view(), name='auth-unlock-user'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
]
