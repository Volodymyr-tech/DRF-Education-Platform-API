from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False, default=[]) #many=True makes the serializer return a list of LessonSerializer objects
    class Meta:
        model = Course
        fields = '__all__'

    def get_quantity_lessons(self, instance):
        return instance.lessons.count() #instatse is the course object and 'lessons' is the related name in the Course model


