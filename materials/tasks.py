from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from materials.models import Course
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


@shared_task
def check_last_course_update(pk):
    course = Course.objects.filter(id=pk).first()
    update_time = timezone.now() - course.last_update
    if update_time >= timedelta(hours=4):
        return True
    else:
        return False