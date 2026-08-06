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

]