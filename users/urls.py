# from django.urls import path
# from .views import (
#     SendOTPView,
#     VerifyOTPView,
#     AdminLoginView,
#     AdminUserListView,
#     AdminUserDetailView,
# )

# urlpatterns = [
#     path("send-otp/", SendOTPView.as_view()),
#     path("verify-otp/", VerifyOTPView.as_view()),
#     path("admin/login/", AdminLoginView.as_view()),
#     path("admin/users/", AdminUserListView.as_view()),
#     path("admin/users/<int:pk>/", AdminUserDetailView.as_view()),
# ]

from django.urls import path
from .views import (
    SendOTPView,
    VerifyOTPView,
    AdminLoginView,
    AdminUserListView,
    AdminUserDetailView,
    AdminTemplateListCreateView,
    AdminTemplateDetailView,
    AdminTemplatePricingListCreateView,
    AdminTemplatePricingDetailView,
    AdminSubscriptionListView,
    AdminSubscriptionStatsView,
    AdminSubscriptionDetailView,
)

urlpatterns = [
    path("send-otp/", SendOTPView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),

    path("admin/login/", AdminLoginView.as_view()),
    path("admin/users/", AdminUserListView.as_view()),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view()),

    # ✅ NEW
    path("admin/templates/", AdminTemplateListCreateView.as_view()),
    path("admin/templates/<int:pk>/", AdminTemplateDetailView.as_view()),

    path("admin/template-pricing/", AdminTemplatePricingListCreateView.as_view()),
    path("admin/template-pricing/<int:pk>/", AdminTemplatePricingDetailView.as_view()),
    # urls.py

    path("admin/subscriptions/", AdminSubscriptionListView.as_view()),
    path("admin/subscriptions/stats/", AdminSubscriptionStatsView.as_view()),
    path("admin/subscriptions/<int:pk>/", AdminSubscriptionDetailView.as_view()),

]
