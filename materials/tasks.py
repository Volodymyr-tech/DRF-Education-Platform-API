from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from materials.models import Course
from users.models import CustomUser




@shared_task
def send_update_mail(pk):
    course = Course.objects.filter(id=pk).first()
    if not course:
        return

    update_time = timezone.now() - course.last_update
    if update_time < timedelta(seconds=4):
        print("Too early to send update mail.")
        return

    subject = "Model name UPDATED"
    message = f"Go via the link and check our update {course.title - course.description}"
    from_email = settings.EMAIL_HOST_USER

    customusers = CustomUser.objects.filter(subscriptions__course=pk)
    print(f"Founded users: {customusers.count()}")
    print(f'{str(customusers.query)}')

    for user in customusers:
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