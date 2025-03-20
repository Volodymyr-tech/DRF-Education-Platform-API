import random
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from materials.models import Course, Lesson
from users.models import Payments, CustomUser

class Command(BaseCommand):
    help = "To generate random payments for users"

    def handle(self, *args, **kwargs):
        users = list(CustomUser.objects.all())
        courses = list(Course.objects.all())
        lessons = list(Lesson.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR("There are not users in the DB!"))
            return

        for _ in range(5):
            user = random.choice(users)
            payment_type = random.choice([Payments.CASH, Payments.TRANSFER])
            amount = round(random.uniform(10, 200), 2)

            # Выбираем случайно: курс или урок
            payed_course = random.choice(courses) if courses and random.choice([True, False]) else None
            payed_lesson = random.choice(lessons) if lessons and payed_course is None else None

            Payments.objects.create(
                user=user,
                pay_data=now(),
                payed_course=payed_course,
                payed_lesson=payed_lesson,
                amount=amount,
                payment_type=payment_type,
            )

        self.stdout.write(self.style.SUCCESS("Payments were successfully generated!"))
