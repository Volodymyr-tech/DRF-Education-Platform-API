from rest_framework import serializers

from .models import CustomUser, Payments


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(
        many=True, read_only=True
    )  # many=True makes the serializer return a list of objects

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "city",
            "avatar",
            "payments",
        ]

    # def create(self, validated_data):


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # tokens = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
        )

    def create(
        self, validated_data
    ):  # if we won't use create method password won't be saved using salt
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserStatisticsSerializer(serializers.ModelSerializer):
    subscriptions_count = serializers.SerializerMethodField()
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "city",
            "avatar",
            "last_login",
            "date_joined",
            "is_active",
            "subscriptions_count",
        ]

    def get_subscriptions_count(self, obj):
        return obj.subscriptions.count()
