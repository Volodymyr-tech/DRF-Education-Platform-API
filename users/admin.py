from django.contrib import admin

from users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
