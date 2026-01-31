from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.views.generic import TemplateView
from materials.models import Course

from .models import CustomUser, Payments
from .serializers import PaymentSerializer, RegisterSerializer, UserProfileSerializer
from .services import StripeTransaction


class RegisterView(CreateAPIView):
    """Registerview class, allow enyone to register"""

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # allow anyone to register


class UserProfileViewSet(viewsets.ModelViewSet):
    """UserviewSet allows only authenticated users and admins to see and make changes in objects.
    Also, you can filter objects by username and email"""

    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "username",
        "email",
    ]
    permission_classes = [IsAuthenticated, IsAdminUser]


class PaymentsListAPIView(generics.ListAPIView):
    """This vies allows authenticated users and admins to watch list of payments objects"""

    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "user__username",
        "user__email",
        "payed_lesson__title",
        "payed_course__title",
        "payment_type",
    ]
    ordering_fields = [
        "pay_data",
    ]
    ordering = ["-pay_data"]
    permission_classes = [IsAuthenticated, IsAdminUser]


class PaymentsCreateAPIView(generics.CreateAPIView):
    """This view allow to create a payment link using Stripe API for authenticated user"""

    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = payment.payed_course if payment.payed_course else payment.payed_lesson
        stripe_product = StripeTransaction.create_product(
            product.title, product.description
        )
        stripe_price = StripeTransaction.create_price(
            stripe_product.name, payment.amount
        )
        stripe_session = StripeTransaction.create_checkout_session(
            "http://127.0.0.1:8000/", stripe_price.id, payment.user.email
        )
        payment.link = stripe_session.url
        payment.save()



class SPAView(TemplateView):
    template_name = "single-page-applicaion.html"
    login_url = '/users/register/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.prefetch_related('modules__lessons').all()
        context['user_subscriptions_ids'] = list(self.request.user.subscriptions.values_list('course_id', flat=True))
        context['courses'] = courses
        return context


class SPAViewSecond(TemplateView):
    template_name = "single-page-application2.html"
    login_url = '/users/register/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.prefetch_related('modules__lessons').all()
        context['user_subscriptions_ids'] = list(self.request.user.subscriptions.values_list('course_id', flat=True))
        context['courses'] = courses
        return context


class LandingPageView(TemplateView):
    template_name = "landing-gold.html"



