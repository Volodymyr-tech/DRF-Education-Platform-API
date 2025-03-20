from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, PaymentsListAPIView, RegisterView, PaymentsCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet) # Register the ViewSet is necessary

app_name = "users"

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments_create'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
