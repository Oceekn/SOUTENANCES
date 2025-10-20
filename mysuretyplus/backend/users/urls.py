from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    ForgotPasswordView,
    ValidateResetTokenView,
    ResetPasswordView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='user-forgot-password'),
    path('validate-reset-token/', ValidateResetTokenView.as_view(), name='user-validate-reset-token'),
    path('reset-password/', ResetPasswordView.as_view(), name='user-reset-password'),
]



