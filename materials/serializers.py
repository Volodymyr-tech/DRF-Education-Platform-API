from rest_framework import serializers

from .models import Course, Lesson, Subscription, MaterialTemplate, MaterialGuide, LawyerCase
from .validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    video_link = serializers.URLField(
        validators=[LinkValidator(link_field="video_link")], required=False
    )

    class Meta:
        model = Lesson
        fields = "__all__"
        # validators = [LinkValidator(link_field="video_link")]

    def get_course(self, instance):
        if instance.course is not None:
            return instance.course.id
        return None


class CourseSerializer(serializers.ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(
        many=True, required=False, default=[], read_only=True
    )  # many=True makes the serializer return a list of LessonSerializer objects
    user_subscription = serializers.SerializerMethodField(
        required=False, read_only=True
    )

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ("created_at",)

    def get_quantity_lessons(self, instance):
        return (
            instance.lessons.count()
        )  # instatse is the course object and 'lessons' is the related name in the Course model

    def get_user_subscription(self, instance):
        request = self.context.get("request")
        if Subscription.objects.filter(user=request.user).exists():
            return True
        else:
            return False


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"


class MaterialTemplateSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = MaterialTemplate
        fields = "__all__"

    def get_file_size(self, obj):
        try:
            return f"{obj.file.size / 1024 / 1024:.2f} MB"
        except:
            return "Unknown"


class MaterialGuideSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = MaterialGuide
        fields = "__all__"

    def get_file_size(self, obj):
        try:
            return f"{obj.file.size / 1024 / 1024:.2f} MB"
        except:
            return "Unknown"


class LawyerCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerCase
        fields = "__all__"
