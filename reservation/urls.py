from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.reservation_view,
        name="reservation",
    ),

    path(
        "blocked-times/",
        views.blocked_times_api,
        name="blocked_times_api",
    ),

    path(
        "cancel/<int:id>/",
        views.cancel_reservation,
        name="cancel_reservation",
    ),

    path(
        "working-hours/",
        views.barber_working_hours,
        name="barber_working_hours",
    ),

   path(
    "payment/",
    views.reservation_payment,
    name="reservation_payment",
),

]