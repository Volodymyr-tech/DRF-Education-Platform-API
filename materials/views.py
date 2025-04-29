from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from users.paginators import StandardResultsSetPagination
from users.permissions import IsModer, IsOwner, IsSubscriber, NotIsModer

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .tasks import send_update_mail


class CourseViewSet(viewsets.ModelViewSet):
    """
    - Authenticated users can view only their courses
    - Moderators and owners can change courses
    - Anyone can create courses
    - Only owners can delete courses
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsModer]

    def get_permissions(self):
        """DRF requires all permissions to return True, and if at least one returns False, it will be 403"""
        if self.action in ["list", "retrieve"]:
            permission_classes = [
                IsAuthenticated,
                IsOwner | IsModer | IsSubscriber,
            ]  # authenticated users can view only their courses
        elif self.action in ["update", "partial_update"]:
            permission_classes = [
                IsAuthenticated,
                IsOwner | IsModer,
            ]  # only moders and owners can change courses
        elif self.action == "create":
            permission_classes = [
                IsAuthenticated,
                NotIsModer,
            ]  # anyone exept moders can create course
        else:
            if self.action == "destroy":
                permission_classes = [
                    IsAuthenticated,
                    IsOwner,
                ]  # only owners can delete courses

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        instance = self.get_object()
        try:
            send_update_mail.delay_on_commit(instance.pk)
        except Exception as e:
            print(e)
        else:
            print("We wont sent message cause update was only few minutes ago")


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    - Authenticated users can view all their lessons and can create new lessons
    - Moders can view ALL lessons, but they are not allowed to create new lessons
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    ordering = ["id"]

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moders").exists():
            return self.queryset.all()
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.groups.filter(name="Moders").exists():
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("Moders cannot create Lessons")


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    - Authenticated object owners can view, update, or delete their lessons
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]
    # pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            permission_classes = [
                IsAuthenticated,
                IsOwner | IsModer,
            ]  # only moder or owners can view or change lessons
        elif self.request.method == "DELETE":
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]  # only owners can delete lessons
        return [permission() for permission in permission_classes]

    # def perform_update(self, serializer):
    #     serializer.save()
    #     send_update_mail.delay_on_commit(self.request.user.pk)


class SubscriptionCreateDestroyAPIView(generics.CreateAPIView, DestroyAPIView):
    """
    - Authenticated users can subscribe to courses
    """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        if Subscription.objects.filter(user=self.request.user, course=course).exists():
            raise PermissionDenied("You are already subscribed to this course")
        serializer.save(user=self.request.user)
