from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .permissions import *
from django.shortcuts import redirect
from core.models import ActivityLog
from django.shortcuts import get_object_or_404
from .models import CustomUser, PhoneVerificationCode
import jdatetime
from django.utils import timezone
from datetime import timedelta
import random
from .sms import send_otp_sms
from .permissions import (
    is_superadmin,
    is_admin,
    is_barber,
)
import jdatetime

@login_required(login_url="/login/")
def profile_view(request):

    from reservation.models import Reservation
    from shop.models import Order
    from academy.models import CourseStudent
    from shop.models import Favorite


    last_reservation = Reservation.objects.filter(
        user=request.user
    ).order_by("-created_at").first()


    last_order = Order.objects.filter(
        user=request.user
    ).order_by("-created_at").first()
    if last_reservation:
             last_reservation.jalali_date = jdatetime.date.fromgregorian(
        date=last_reservation.date
    ).strftime("%Y/%m/%d")

    if last_order:
        last_order.jalali_date = jdatetime.datetime.fromgregorian(
        datetime=last_order.created_at
    ).strftime("%Y/%m/%d")



    context = {


        "reservation_count": Reservation.objects.filter(
            user=request.user
        ).count(),



        "order_count": Order.objects.filter(
            user=request.user
        ).count(),



        "course_count": CourseStudent.objects.filter(
            user=request.user
        ).count(),

        "favorite_count": Favorite.objects.filter(
            user=request.user
        ).count(),


        "last_reservation": last_reservation,


        "last_order": last_order,


    }


    return render(
        request,
        "user/profile.html",
        context
    )
def logout_view(request):

    logout(request)

    return redirect("/")
def register_view(request):

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]
            full_name = form.cleaned_data["full_name"]

            # حذف کدهای قبلی این شماره
            PhoneVerificationCode.objects.filter(
                phone=phone,
                is_used=False
            ).update(
                is_used=True
            )

            # ساخت کد ۶ رقمی
            code = str(
                random.randint(100000, 999999)
            )

            # ذخیره کد
            PhoneVerificationCode.objects.create(
                phone=phone,
                code=code,
                expires_at=timezone.now() + timedelta(minutes=5)
            )

            # ارسال SMS
            response = send_otp_sms(
                phone,
                code
            )

            # اگر ارسال SMS شکست خورد
            if response is None or not response.ok:

                messages.error(
                    request,
                    "ارسال کد تأیید با مشکل مواجه شد. لطفاً بعداً تلاش کنید."
                )

                return redirect("register")

            # اطلاعات ثبت نام را موقتاً در session نگه می‌داریم
            request.session["pending_registration"] = {
                "phone": phone,
                "full_name": full_name,
                "password": password,
            }

            return redirect("verify_phone")

        else:

            print(
                "REGISTER FORM ERRORS:",
                form.errors
            )

    return render(
        request,
        "core/auth.html",
        {
            "form": form,
            "mode": "register",
        }
    )
def verify_phone(request):

    pending_registration = request.session.get(
        "pending_registration"
    )

    if not pending_registration:
        return redirect("register")

    phone = pending_registration["phone"]

    if request.method == "POST":

        entered_code = request.POST.get(
            "code",
            ""
        ).strip()

        verification = (
            PhoneVerificationCode.objects
            .filter(
                phone=phone,
                is_used=False
            )
            .order_by("-created_at")
            .first()
        )

        if not verification:

            messages.error(
                request,
                "کد تأیید یافت نشد."
            )

        elif verification.is_expired():

            messages.error(
                request,
                "کد تأیید منقضی شده است."
            )

        elif verification.attempts >= 5:

            messages.error(
                request,
                "تعداد تلاش‌های مجاز تمام شده است."
            )

        elif verification.code != entered_code:

            verification.attempts += 1

            verification.save(
                update_fields=["attempts"]
            )

            messages.error(
                request,
                "کد تأیید اشتباه است."
            )

        else:

            # کد صحیح است
            verification.is_used = True

            verification.save(
                update_fields=["is_used"]
            )

            # حالااااا کاربر ساخته می‌شود
            user = CustomUser(
                phone=pending_registration["phone"],
                full_name=pending_registration["full_name"],
                phone_verified=True,
            )

            user.set_password(
                pending_registration["password"]
            )

            user.save()

            # پاک کردن اطلاعات موقت ثبت نام
            request.session.pop(
                "pending_registration",
                None
            )

            ActivityLog.objects.create(
                user=user,
                action=f"{user.full_name} شماره موبایل خود را تأیید کرد"
            )

            # ورود خودکار
            login(
                request,
                user,
                backend="users.backends.PhoneBackend"
            )

            next_url = request.session.pop(
                "login_next",
                None
            )

            return redirect(
                next_url or "/"
            )

    return render(
        request,
        "core/verify_phone.html",
        {
            "phone": phone,
        }
    )
def login_view(request):

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":

        phone = request.POST.get("phone")
        password = request.POST.get("password")

        user = authenticate(
            request,
            phone=phone,
            password=password
        )

        if user is not None:

            if not user.phone_verified:

                request.session["pending_verification_user_id"] = user.id

                if next_url:
                    request.session["login_next"] = next_url

                return redirect("verify_phone")

            login(request, user)

            return redirect(next_url or "/")

        else:

            messages.error(
                request,
                "شماره موبایل یا رمز عبور اشتباه است."
            )

    return render(
        request,
        "core/auth.html",
        {
            "mode": "login",
            "next": next_url,
        }
    )
@login_required(login_url="/login/")
def upload_profile_image(request):

    if request.method == "POST":

        if request.FILES.get("profile_image"):

            request.user.profile_image = request.FILES["profile_image"]

            request.user.save()

    return redirect("profile")

@login_required(login_url="/login/")
def update_profile(request):

    if request.method == "POST":

        request.user.full_name = request.POST.get("full_name") or request.user.full_name
        request.user.phone = request.POST.get("phone") or request.user.phone
        request.user.address = request.POST.get("address") or request.user.address
        request.user.birth_date = request.POST.get("birth_date") or request.user.birth_date
        request.user.marriage_date = request.POST.get("marriage_date") or request.user.marriage_date
        request.user.child_birth = request.POST.get("child_birth") or request.user.child_birth

        request.user.save()

    return redirect("profile")

@login_required(login_url="/login/")
def profile_data(request):
    return JsonResponse({
        "full_name": request.user.full_name,        "phone": request.user.phone,        "address": request.user.address or "",        "birth_date": str(request.user.birth_date or ""),        "marriage_date": str(request.user.marriage_date or ""),        "child_birth": str(request.user.child_birth or ""),        "profile_image": request.user.profile_image.url if request.user.profile_image else "",
    })

@login_required(login_url="/login/")
def dashboard(request):

    print(request.user)
    print(request.user.groups.all())

    if is_superadmin(request.user):
        return redirect("superadmin_dashboard")

    elif is_admin(request.user):
        return redirect("superadmin_dashboard")

    elif is_barber(request.user):
        return redirect("superadmin_dashboard")

    return redirect("profile")

from shop.models import Order
@login_required(login_url="/login/")
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    for order in orders:
        order.jalali_date = jdatetime.datetime.fromgregorian(
            datetime=order.created_at
        ).strftime("%Y/%m/%d")

    return render(
        request,
        "user/orders.html",
        {
            "orders": orders,
        }
    )

from django.shortcuts import get_object_or_404
from shop.models import Order

@login_required(login_url="/login/")
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )


    return render(
        request,
        "user/order_detail.html",
        {
            "order": order,
        }
    )

from reservation.models import Reservation
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def my_bookings(request):

    reservations = Reservation.objects.filter(
        user=request.user
    ).order_by("-created_at")

    for reservation in reservations:
        reservation.jalali_date = jdatetime.date.fromgregorian(
            date=reservation.date
        ).strftime("%Y/%m/%d")

    return render(
        request,
        "user/my_bookings.html",
        {
            "reservations": reservations
        }
    )
from django.shortcuts import get_object_or_404


@login_required(login_url="/login/")
def reservation_detail(request, id):

    reservation = get_object_or_404(
        Reservation,
        id=id,
        user=request.user
    )

    return render(
        request,
        "user/reservation_detail.html",
        {
            "reservation": reservation
        }
    )

from academy.models import CourseStudent


@login_required(login_url="/login/")
def my_courses(request):

    courses = CourseStudent.objects.filter(
        user=request.user
    ).select_related(
        "course"
    )

    return render(
        request,
        "user/my_courses.html",
        {
            "courses": courses,
        }
    )

from academy.models import CourseStudent
def user_course_detail(request, id):

    course_student = get_object_or_404(
        CourseStudent,
        course_id=id,
        user=request.user
    )

    course = course_student.course

    sessions = course.sessions.all().order_by("order")


    total_sessions = sessions.count()


    completed_sessions = SessionProgress.objects.filter(
        student=course_student
    ).count()


    if total_sessions > 0:
        progress = int(
            (completed_sessions / total_sessions) * 100
        )
    else:
        progress = 0



    return render(
        request,
        "user/course_detail.html",
        {
            "course": course,
            "course_student": course_student,
            "sessions": sessions,
            "progress": progress,
        }
    )
from academy.models import CourseSession, CourseStudent, SessionProgress
def session_detail(request, id):

    session = get_object_or_404(
        CourseSession,
        id=id
    )


    course_student = get_object_or_404(
        CourseStudent,
        course=session.course,
        user=request.user
    )


    SessionProgress.objects.get_or_create(
        student=course_student,
        session=session
    )


    previous_session = (
        CourseSession.objects
        .filter(
            course=session.course,
            order__lt=session.order
        )
        .order_by("-order")
        .first()
    )


    next_session = (
        CourseSession.objects
        .filter(
            course=session.course,
            order__gt=session.order
        )
        .order_by("order")
        .first()
    )


    return render(
        request,
        "user/session_detail.html",
        {
            "session": session,
            "course": session.course,
            "previous_session": previous_session,
            "next_session": next_session,
        }
    )

from shop.models import Favorite
from academy.models import CourseFavorite
@login_required(login_url="/login/")
def my_favorites(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related("product")


    course_favorites = CourseFavorite.objects.filter(
        user=request.user
    ).select_related("course")


    return render(
        request,
        "user/my_favorites.html",
        {
            "favorites": favorites,
            "course_favorites": course_favorites
        }
    )

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required(login_url="/login/")
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "رمز عبور با موفقیت تغییر کرد."
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(
            user=request.user
        )


    return render(
        request,
        "user/change_password.html",
        {
            "form": form
        }
    )