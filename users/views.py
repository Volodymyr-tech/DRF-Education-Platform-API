from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import CustomUser, Payments
from .serializers import UserProfileSerializer, PaymentSerializer, RegisterSerializer

from rest_framework.permissions import AllowAny

from .services import StripeTransaction


class RegisterView(CreateAPIView):
    '''Registerview class, allow enyone to register'''
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # allow anyone to register


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email',]
    permission_classes = [IsAuthenticated, IsAdminUser]



class PaymentsListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'user__email', 'payed_lesson__title', 'payed_course__title', 'payment_type']
    ordering_fields = ['pay_data',]
    ordering = ['-pay_data']
    permission_classes = [IsAuthenticated, IsAdminUser]


class PaymentsCreateAPIView(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    #permission_classes = [IsAuthenticated, IsAdminUser]


    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = payment.payed_course if payment.payed_course else payment.payed_lesson
        stripe_product = StripeTransaction.create_product(product.title, product.description)
        stripe_price = StripeTransaction.create_price(stripe_product.name, payment.amount)
        stripe_session = StripeTransaction.create_checkout_session('http://127.0.0.1:8000/', stripe_price.id, payment.user.email)
        payment.link = stripe_session.url
        payment.save()