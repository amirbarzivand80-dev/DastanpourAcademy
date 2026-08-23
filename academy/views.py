from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from core.offer_utils import get_course_offer_price
from .models import Course, CourseStudent
from django.contrib.auth.decorators import login_required
from academy.models import CourseStudent


def education(request):

    courses = Course.objects.filter(
        is_active=True
    )

    for course in courses:

        offer_price = get_course_offer_price(course)

        course.offer_has_discount = offer_price["has_offer"]
        course.offer_discount_percent = offer_price["discount_percent"]
        course.offer_old_price = offer_price["old_price"]
        course.offer_new_price = offer_price["new_price"]

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

    offer_price = get_course_offer_price(course)

    if offer_price["has_offer"]:
        final_price = offer_price["new_price"]
    else:
        final_price = course.price

    return render(
        request,
        "core/course_detail.html",
        {
            "course": course,
            "offer_price": offer_price,
            "final_price": final_price,
        }
    )

@login_required(login_url="/login/")
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
@login_required(login_url="/login/")
def course_payment(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    # =====================================================
    # قیمت پایه دوره با درنظر گرفتن پیشنهاد ویژه
    # =====================================================

    offer_price = get_course_offer_price(course)

    if offer_price["has_offer"]:
        base_price = offer_price["new_price"]
    else:
        base_price = course.price

    final_price = base_price

    discount_amount = 0
    discount_code = request.session.get(
        "course_discount_code"
    )

    discount_error = None
    discount_success = None

    # =====================================================
    # اعمال کد تخفیف
    # =====================================================

    if request.method == "POST":

        code = request.POST.get(
            "discount_code",
            ""
        ).strip().upper()

        # حذف تخفیف قبلی
        request.session.pop(
            "course_discount_code",
            None
        )

        request.session.pop(
            "course_discount_amount",
            None
        )

        if not code:

            discount_error = "کد تخفیف را وارد کنید."

        else:

            from discounts.models import DiscountCode
            from discounts.models import DiscountUsage

            try:

                discount = DiscountCode.objects.get(
                    code=code
                )

            except DiscountCode.DoesNotExist:

                discount_error = (
                    "کد تخفیف وارد شده معتبر نیست."
                )

            else:

                # -----------------------------------------
                # اعتبار کلی
                # -----------------------------------------

                if not discount.is_valid_now():

                    discount_error = (
                        "این کد تخفیف فعال یا معتبر نیست."
                    )

                else:

                    # -------------------------------------
                    # محدودیت استفاده کاربر
                    # -------------------------------------

                    user_usage_count = DiscountUsage.objects.filter(
                        discount=discount,
                        user=request.user
                    ).count()

                    if (
                        discount.per_user_limit is not None
                        and user_usage_count >= discount.per_user_limit
                    ):

                        discount_error = (
                            "شما قبلاً به تعداد مجاز از این کد استفاده کرده‌اید."
                        )

                    # -------------------------------------
                    # کاربران خاص
                    # -------------------------------------

                    elif (
                        discount.users.exists()
                        and not discount.users.filter(
                            id=request.user.id
                        ).exists()
                    ):

                        discount_error = (
                            "این کد تخفیف برای حساب شما قابل استفاده نیست."
                        )

                    # -------------------------------------
                    # حداقل خرید
                    # -------------------------------------

                    elif (
                        discount.minimum_purchase
                        and base_price < discount.minimum_purchase
                    ):

                        discount_error = (
                            f"حداقل مبلغ خرید برای این کد "
                            f"{discount.minimum_purchase:,} تومان است."
                        )

                    # -------------------------------------
                    # بررسی محدوده دوره
                    # -------------------------------------

                    else:

                        eligible = False

                        if discount.courses_all:

                            eligible = True

                        elif discount.courses.filter(
                            id=course.id
                        ).exists():

                            eligible = True

                        if not eligible:

                            discount_error = (
                                "این کد تخفیف برای این دوره قابل استفاده نیست."
                            )

                        else:

                            # -----------------------------
                            # محاسبه تخفیف
                            # -----------------------------

                            if discount.discount_type == "percent":

                                discount_amount = (
                                    base_price
                                    * discount.value
                                    // 100
                                )

                            else:

                                discount_amount = min(
                                    discount.value,
                                    base_price
                                )

                            final_price = max(
                                base_price - discount_amount,
                                0
                            )

                            # -----------------------------
                            # ذخیره در Session
                            # -----------------------------

                            request.session[
                                "course_discount_code"
                            ] = discount.code

                            request.session[
                                "course_discount_amount"
                            ] = discount_amount

                            discount_code = discount.code

                            discount_success = (
                                "کد تخفیف با موفقیت اعمال شد."
                            )

    # =====================================================
    # اگر قبلاً کد برای همین دوره اعمال شده
    # =====================================================

    elif discount_code:

        try:

            from discounts.models import DiscountCode

            discount = DiscountCode.objects.get(
                code=discount_code
            )

            if discount.is_valid_now():

                # اطمینان از اینکه کد برای این دوره است
                if (
                    discount.courses_all
                    or discount.courses.filter(
                        id=course.id
                    ).exists()
                ):

                    discount_amount = request.session.get(
                        "course_discount_amount",
                        0
                    )

                    final_price = max(
                        base_price - discount_amount,
                        0
                    )

                else:

                    request.session.pop(
                        "course_discount_code",
                        None
                    )

                    request.session.pop(
                        "course_discount_amount",
                        None
                    )

                    discount_code = None

            else:

                request.session.pop(
                    "course_discount_code",
                    None
                )

                request.session.pop(
                    "course_discount_amount",
                    None
                )

                discount_code = None

        except DiscountCode.DoesNotExist:

            request.session.pop(
                "course_discount_code",
                None
            )

            request.session.pop(
                "course_discount_amount",
                None
            )

            discount_code = None

    return render(
        request,
        "core/course_payment.html",
        {
            "course": course,
            "offer_price": offer_price,
            "base_price": base_price,
            "final_price": final_price,
            "discount_code": discount_code,
            "discount_amount": discount_amount,
            "discount_error": discount_error,
            "discount_success": discount_success,
        }
    )

from users.sms import send_course_confirmation_sms


def course_payment_success(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    # =========================================
    # محاسبه مبلغ نهایی دوره
    # =========================================

    offer_price = get_course_offer_price(course)

    if offer_price["has_offer"]:
        base_price = offer_price["new_price"]
    else:
        base_price = course.price

    discount_amount = request.session.get(
        "course_discount_amount",
        0
    )

    final_price = max(
        base_price - discount_amount,
        0
    )

    # =========================================
    # ثبت هنرجو
    # =========================================

    student, created = CourseStudent.objects.get_or_create(
        user=request.user,
        course=course
    )

    # =========================================
    # ارسال پیامک فقط یک بار
    # =========================================

    if created:

        send_course_confirmation_sms(
            phone=request.user.phone,
            name=request.user.full_name,
            course=course.title,
            teacher=course.teacher,
            price=final_price,
        )

    # =========================================
    # پاک کردن تخفیف بعد از ثبت موفق
    # =========================================

    request.session.pop(
        "course_discount_code",
        None
    )

    request.session.pop(
        "course_discount_amount",
        None
    )

    return redirect(
        "course_detail",
        slug=course.slug
    )