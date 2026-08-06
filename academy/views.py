from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Course, CourseStudent
from django.contrib.auth.decorators import login_required
from academy.models import CourseStudent



def education(request):

    courses = Course.objects.filter(
        is_active=True
    )

    return render(
        request,
        "core/education.html",
        {
            "courses": courses,
            "course_types": [
                ("offline", "دوره‌های حضوری"),
                ("online", "دوره‌های آنلاین"),
                ("free", "آموزش‌های رایگان"),
            ]
        }
    )


def course_detail(request, slug):

    course = get_object_or_404(
        Course,
        slug=slug,
        is_active=True
    )

    return render(
        request,
        "core/course_detail.html",
        {
            "course": course,
        }
    )


@login_required
def course_register(request, slug):

    course = get_object_or_404(
        Course,
        slug=slug
    )

    if CourseStudent.objects.filter(
        course=course,
        user=request.user
    ).exists():

        messages.warning(
            request,
            "شما قبلاً در این دوره ثبت‌نام کرده‌اید."
        )

        return redirect(
            "course_detail",
            slug=course.slug
        )


    if course.course_type == "free":

        CourseStudent.objects.create(
            course=course,
            user=request.user,
            is_paid=True
        )

        messages.success(
            request,
            "ثبت‌نام شما با موفقیت انجام شد."
        )

        return redirect(
            "course_detail",
            slug=course.slug
        )


    return redirect(
        "course_payment",
        course_id=course.id
    )


@login_required
def my_courses(request):

    courses = CourseStudent.objects.filter(
        user=request.user,
        is_paid=True
    ).select_related("course")

    return render(
        request,
        "academy/my_courses.html",
        {
            "courses": courses,
        }
    )

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Course, CourseFavorite
@login_required(login_url="/login/")
def toggle_course_favorite(request, id):

    course = Course.objects.get(id=id)

    favorite, created = CourseFavorite.objects.get_or_create(
        user=request.user,
        course=course
    )

    if not created:
        favorite.delete()

    return JsonResponse({
        "status": "ok"
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, CourseStudent


def course_payment(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    return render(
        request,
       "core/course_payment.html",
        {
            "course": course
        }
    )


def course_payment_success(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    CourseStudent.objects.get_or_create(
        user=request.user,
        course=course
    )

    return redirect(
        "course_detail",
        slug=course.slug
    )