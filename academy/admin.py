from django.contrib import admin
from .models import (
    Course,
    CourseSession,
    CourseStudent,
    CourseTopic,
    CourseFeature,
    CourseImage,
)


class CourseSessionInline(admin.TabularInline):
    model = CourseSession
    extra = 1

class CourseTopicInline(admin.TabularInline):
    model = CourseTopic
    extra = 1


class CourseFeatureInline(admin.TabularInline):
    model = CourseFeature
    extra = 1


class CourseImageInline(admin.TabularInline):
    model = CourseImage
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "course_type",
        "price",
        "is_active",
    )

    list_filter = (
        "course_type",
        "is_active",
    )

    search_fields = (
        "title",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [
    CourseSessionInline,
    CourseTopicInline,
    CourseFeatureInline,
    CourseImageInline,
]


@admin.register(CourseStudent)
class CourseStudentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "course",
        "is_paid",
        "created_at",
    )

    list_filter = (
        "is_paid",
        "course",
    )

    search_fields = (
        "user__full_name",
        "course__title",
    )

from .models import CourseFavorite


@admin.register(CourseFavorite)
class CourseFavoriteAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "course",
        "created_at",
    )