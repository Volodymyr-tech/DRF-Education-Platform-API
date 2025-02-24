from rest_framework import serializers
from .models import CustomUser, Payments

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'city', 'avatar', 'payments']



