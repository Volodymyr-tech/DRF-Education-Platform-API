from django.contrib import admin

from materials.models import Course, Lesson, Subscription, Module, MaterialTemplate, MaterialGuide, LawyerCase


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


@admin.register(MaterialTemplate)
class MaterialTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
    )

@admin.register(MaterialGuide)
class MaterialGuideAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
    )


@admin.register(LawyerCase)
class LawyerCaseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "preview",
    )