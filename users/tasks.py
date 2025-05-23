from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def check_last_login():
    inactive_cutoff = timezone.now() - timedelta(days=30)
    CustomUser.objects.filter(is_active=True, last_login__lt=inactive_cutoff).update(
        is_active=False
    )
