from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import CustomUser, Payments
from .serializers import UserProfileSerializer, PaymentSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'payed_course']



class PaymentsListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'user__email', 'payed_lesson__title', 'payed_course__title', 'payment_type']
    ordering_fields = ['pay_data',]
    ordering = ['-pay_data']