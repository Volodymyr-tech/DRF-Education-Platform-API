from django.urls import path

from .views import (
    LandingPageView, SPAViewSecond,
    AuthLoginView,
)

app_name = "users"

urlpatterns = [
    path("auth-login/", AuthLoginView.as_view(), name="auth-login"),
    path("spa-2/", SPAViewSecond.as_view(), name="spa2"),
    path("landing/", LandingPageView.as_view(), name="landing"),
]
