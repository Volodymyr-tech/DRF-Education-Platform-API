from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Payments

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)  # many=True makes the serializer return a list of objects

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'city', 'avatar', 'payments']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # tokens = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password',)

    # def get_tokens(self, user):
    #     refresh = RefreshToken.for_user(user)
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token),
    #     }
    #
    def create(self, validated_data):  # if we won't use create method password won't be saved using salt
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

