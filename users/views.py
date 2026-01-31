from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView # Added
from rest_framework.response import Response # Added
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView

from materials.models import Course, Subscription

from .models import CustomUser, Payments
from .serializers import PaymentSerializer, RegisterSerializer, UserProfileSerializer
from .services import StripeTransaction


class RegisterView(CreateAPIView):
    """Registerview class, allow enyone to register"""

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # allow anyone to register

    def perform_create(self, serializer):
        user = serializer.save()
        course = Course.objects.filter(title="Вводный курс: Основы ВНЖ").first()
        if course:
            Subscription.objects.create(user=user, course=course)


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


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        # Добавляем ID курсов, на которые подписан пользователь, для удобства фронтенда
        data = serializer.data
        data['subscriptions_ids'] = list(request.user.subscriptions.values_list('course_id', flat=True))
        return Response(data)


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



class SPAViewSecond(LoginRequiredMixin, TemplateView):
    template_name = "single-page-application2.html"
    login_url = '/api/users/auth-login/'  # Перенаправление на вашу страницу входа

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.prefetch_related('modules__lessons').all()
        
        # Для REST подхода мы не можем полагаться на request.user здесь, 
        # так как аутентификация происходит через JWT на клиенте.
        # Передаем пустой список, он будет обновлен JS-ом.
        context['user_subscriptions_ids'] = [] 
        if self.request.user.is_authenticated:
             context['user_subscriptions_ids'] = list(self.request.user.subscriptions.values_list('course_id', flat=True))

        context['courses'] = courses
        return context


class LandingPageView(TemplateView):
    template_name = "landing-gold.html"



class AuthLoginView(TemplateView):
    template_name = "auth-login.html"


class SessionTokenObtainPairView(TokenObtainPairView):
    """
    Возвращает JWT токен И устанавливает сессию Django (sessionid cookie).
    Это нужно, чтобы работали и API запросы, и LoginRequiredMixin в TemplateView.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # 1. Стандартная логика получения токена
        response = super().post(request, *args, **kwargs)

        # 2. Если токен выдан успешно, логиним пользователя в сессию
        if response.status_code == 200:
            # Получаем данные из запроса для аутентификации сессии
            email = request.data.get('email')
            password = request.data.get('password')
            
            # Важно: authenticate проверяет credentials и возвращает объект user
            # Убедитесь, что в request.data приходят правильные поля (email/password)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)  # Эта команда устанавливает sessionid cookie
        
        return response
