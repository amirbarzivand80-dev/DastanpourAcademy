from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = (
        "phone",
        "full_name",
        "is_staff",
        "is_superuser",
    )

    ordering = ("phone",)

    fieldsets = (
        (None, {
            "fields": (
                "phone",
                "password",
                "full_name",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),

            "fields": (
                "phone",
                "full_name",
                "password1",
                "password2",
                "is_staff",
                "is_superuser",
            ),
        }),
    )

    search_fields = (
        "phone",
        "full_name",
    )