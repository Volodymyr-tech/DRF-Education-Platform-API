from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False, default=[], read_only=True) #many=True makes the serializer return a list of LessonSerializer objects

    class Meta:
        model = Course
        fields = '__all__'


    def get_quantity_lessons(self, instance):
        return instance.lessons.count() #instatse is the course object and 'lessons' is the related name in the Course model


    # def create(self, validated_data):
    #     lessons_data = validated_data.pop('lessons', None)  # getting info about lessons from the validated_data
    #     course = Course.objects.create(**validated_data)  # creating a course with the validated data
    #
    #     if lessons_data:  # if there are lessons, create them for the course
    #         for lesson_data in lessons_data:
    #             Lesson.objects.create(course=course, **lesson_data)  # creating lessons for the course
    #
    #     return course
    #
    #
    # def update(self, instance, validated_data):
    #     lessons_data = validated_data.pop('lessons', [])  # getting info about lessons from the validated_data
    #     instance.update(**validated_data)  # updating the course with the validated data
    #
    #     for lesson_data in lessons_data:
    #         if 'id' in lesson_data:  # if the lesson has an id, it means it already exists in the database
    #             lesson = Lesson.objects.get(id=lesson_data.pop('id'))
    #             lesson.update(**lesson_data)
    #         else:
    #             Lesson.objects.create(course=instance, **lesson_data)  # creating a new lesson for the course
    #
    #     return instance
