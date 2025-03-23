from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.paginators import StandardResultsSetPagination
from users.permissions import IsOwner, IsModer, NotIsModer
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsModer]


    def get_permissions(self):
        """DRF requires all permissions to return True, and if at least one returns False, it will be 403"""
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated, IsOwner | IsModer]  # authenticated users can view only their courses
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwner | IsModer] # only moders and owners can change courses
        elif self.action == "create":
            permission_classes = [IsAuthenticated, NotIsModer]  # anyone exept moders can create course
        else:
            if self.action == "destroy":
                permission_classes = [IsAuthenticated, IsOwner]  # only owners can delete courses


        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    #pagination_class = StandardResultsSetPagination
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
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]
    #pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            permission_classes = [IsAuthenticated, IsOwner | IsModer]  # only moder or owners can view or change lessons
        elif self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsOwner]  # only owners can delete lessons
        return [permission() for permission in permission_classes]


class SubscriptionCreateDestroyAPIView(generics.CreateAPIView, DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if Subscription.objects.filter(user=self.request.user, course=course).exists():
            raise PermissionDenied("You are already subscribed to this course")
        serializer.save(user=self.request.user)

