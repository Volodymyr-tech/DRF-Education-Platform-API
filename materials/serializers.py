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

    def get_course(self, instance):
        if instance.course is not None:
            return instance.course.id
        return None


class CourseSerializer(serializers.ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(
        many=True, required=False, default=[], read_only=True
    )
    user_subscription = serializers.SerializerMethodField(
        required=False, read_only=True
    )

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ("created_at",)

    def get_quantity_lessons(self, instance):
        return instance.lessons.count()

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


# --- Templates ---

class MaterialTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTemplate
        fields = ['id', 'title', 'description', 'created_at']

class MaterialTemplateDetailSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = MaterialTemplate
        fields = "__all__"

    def get_file_size(self, obj):
        try:
            return f"{obj.file.size / 1024 / 1024:.2f} MB"
        except:
            return "Unknown"


# --- Guides ---

class MaterialGuideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialGuide
        fields = ['id', 'title', 'description', 'created_at']

class MaterialGuideDetailSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = MaterialGuide
        fields = "__all__"

    def get_file_size(self, obj):
        try:
            return f"{obj.file.size / 1024 / 1024:.2f} MB"
        except:
            return "Unknown"


# --- Lawyer Cases ---

class LawyerCaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerCase
        fields = ['id', 'title', 'description', 'preview', 'created_at']

class LawyerCaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerCase
        fields = "__all__"
