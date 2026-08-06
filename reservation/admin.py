from django.contrib import admin
from .models import Reservation, Barber


@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "is_active",
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "service",
        "barber",
        "date",
        "time",
        "status",
    )

    list_filter = (
        "status",
        "date",
        "barber",
    )