from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Payments
from .serializers import UserProfileSerializer, PaymentSerializer, RegisterSerializer

from rest_framework.permissions import AllowAny

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # allow anyone to register


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email',]
    permission_classes = [IsAuthenticated]



class PaymentsListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'user__email', 'payed_lesson__title', 'payed_course__title', 'payment_type']
    ordering_fields = ['pay_data',]
    ordering = ['-pay_data']
    permission_classes = [IsAuthenticated]
