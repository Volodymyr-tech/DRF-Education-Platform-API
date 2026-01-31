from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
    SubscriptionCreateDestroyAPIView,
    MaterialTemplateViewSet,
    MaterialGuideViewSet,
    LawyerCaseViewSet,
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"templates", MaterialTemplateViewSet)
router.register(r"guides", MaterialGuideViewSet)
router.register(r"lawyer-cases", LawyerCaseViewSet)

app_name = "materials"

urlpatterns = [
    path("", include(router.urls)),  # Include the generated API endpoints
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lesson-detail",
    ),
    path(
        "subscriptions/create/",
        SubscriptionCreateDestroyAPIView.as_view(),
        name="subscription-create",
    ),
    path(
        "subscriptions/delete/<int:pk>/",
        SubscriptionCreateDestroyAPIView.as_view(),
        name="subscription-delete",
    ),
]
