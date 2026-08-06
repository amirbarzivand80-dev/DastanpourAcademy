from django.urls import path
from . import views

urlpatterns = [

    path("", views.services_view, name="services"),

    path(
        "detail/<int:id>/",
        views.service_detail,
        name="service_detail"
    ),

]