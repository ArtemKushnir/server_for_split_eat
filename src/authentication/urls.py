from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import GetStatusView, ConfirmEmailView, RegisterView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", RegisterView.as_view()),
    path("confirm-email/", ConfirmEmailView.as_view()),
    path("get-user-status/", GetStatusView.as_view()),
]
