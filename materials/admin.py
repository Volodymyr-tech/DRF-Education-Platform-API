from django.contrib import admin

from materials.models import Course, Lesson, Subscription, Module


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "description",
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "description",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "course",
    )
