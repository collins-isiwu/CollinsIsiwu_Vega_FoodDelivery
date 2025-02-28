from django.urls import path
from .views import UserRegistrationView, UserLoginView, AdminRegistrationView, PasswordResetRequestView, PasswordResetView, LogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/admin/', AdminRegistrationView.as_view(), name='register_admin'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/verify/', PasswordResetView.as_view(), name='password_reset_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
