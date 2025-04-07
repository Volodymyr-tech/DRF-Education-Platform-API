from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from users.models import CustomUser




@shared_task
def send_update_mail(pk):
    subject = "Model name UPDATED"
    message = "Go via the link and check our update"
    from_email = settings.EMAIL_HOST_USER

    print("SMTP From Email:", from_email)

    customusers = CustomUser.objects.filter(subscriptions__course=pk)
    print(f"Founded users: {customusers.count()}")

    for user in customusers:
        # Отправка письма
        try:
            send_mail(
                subject,
                message,
                from_email,
                [user.email],
                fail_silently=False,
            )
            print(f"Message to {user.email} was sent")
        except Exception as e:
            print(e)


