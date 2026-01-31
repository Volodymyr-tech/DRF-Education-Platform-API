from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    PaymentsCreateAPIView,
    PaymentsListAPIView,
    RegisterView,
    UserProfileViewSet,
    LandingPageView, SPAViewSecond,
    CurrentUserView, AuthLoginView,
    SessionTokenObtainPairView,  # Импортируем наш новый класс
)

router = DefaultRouter()
router.register(r"profiles", UserProfileViewSet)  # Register the ViewSet is necessary

app_name = "users"

urlpatterns = [
    path("", include(router.urls)),
    path("auth-login/", AuthLoginView.as_view(), name="auth-login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
    path(
        "login/",
        SessionTokenObtainPairView.as_view(), # Используем гибридный вход
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("spa-2/", SPAViewSecond.as_view(), name="spa2"),
    path("landing/", LandingPageView.as_view(), name="landing"),
    path("me/", CurrentUserView.as_view(), name="current_user"), # Added
]
