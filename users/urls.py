from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, PaymentsListAPIView

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet) # Register the ViewSet is necessary


urlpatterns = [
    path('', include(router.urls)),
    path('payments/', PaymentsListAPIView.as_view(), name='payments'),
]
