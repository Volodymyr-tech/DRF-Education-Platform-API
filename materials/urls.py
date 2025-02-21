from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonRetrieveUpdateDestroyAPIView, LessonListCreateAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet) # Automatically generate API endpoints for CourseViewSet

urlpatterns = [
    path('', include(router.urls)), # Include the generated API endpoints
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
]
