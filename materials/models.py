from django.db import models

from users.models import CustomUser


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(CustomUser, null=True, blank=True, related_name='course', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_link = models.URLField(blank=True)
    owner = models.ForeignKey(CustomUser, null=True, blank=True, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.course.title})"



class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, related_name='subscriptions', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='subscribers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

