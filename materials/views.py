from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner, IsModer
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


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
            permission_classes = [IsAuthenticated, ~IsModer]  # anyone exept moders can create course
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

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moders").exists():
            return self.queryset.all()
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            permission_classes = [IsAuthenticated, IsOwner | IsModer]  # only moder or owners can view or change lessons
        elif self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsOwner]  # only owners can delete lessons
        return [permission() for permission in permission_classes]