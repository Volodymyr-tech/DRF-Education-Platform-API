from django.contrib import admin

from users.models import CustomUser, Payments


# Register your models here.
@admin.register(CustomUser)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payed_course', 'payed_lesson', 'amount')