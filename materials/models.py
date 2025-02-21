from django.db import models



class Course(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="materials/avatars/", blank=True, null=True)
    description = models.TextField()


    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="materials/avatars/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)