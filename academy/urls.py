from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.education,
        name="education"
    ),

    path(
        "register/<slug:slug>/",
        views.course_register,
        name="course_register"
    ),

    path(
        "my-courses/",
        views.my_courses,
        name="my_courses"
    ),

    path(
        "course-favorite/<int:id>/",
        views.toggle_course_favorite,
        name="toggle_course_favorite"
    ),

    path(
        "course/payment/<int:course_id>/",
        views.course_payment,
        name="course_payment"
    ),

    path(
        "course/payment/success/<int:course_id>/",
        views.course_payment_success,
        name="course_payment_success"
    ),

    path(
        "<slug:slug>/",
        views.course_detail,
        name="course_detail"
    ),

]