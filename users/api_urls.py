from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    PaymentsCreateAPIView,
    PaymentsListAPIView,
    RegisterView,
    UserProfileViewSet,
    CurrentUserView,
    SessionTokenObtainPairView,
    UserStatisticsListView, # Added
)

router = DefaultRouter()
router.register(r"profiles", UserProfileViewSet)

app_name = "users_api"

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
    path(
        "login/",
        SessionTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", CurrentUserView.as_view(), name="current_user"),
    path("users-stats/", UserStatisticsListView.as_view(), name="users_stats"), # Added
]
