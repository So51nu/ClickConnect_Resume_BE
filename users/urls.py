from django.urls import path
from .views import (
    SendOTPView,
    VerifyOTPView,
    AdminLoginView,
    AdminUserListView,
    AdminUserDetailView,
)

urlpatterns = [
    path("send-otp/", SendOTPView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("admin/login/", AdminLoginView.as_view()),
    path("admin/users/", AdminUserListView.as_view()),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view()),
]
