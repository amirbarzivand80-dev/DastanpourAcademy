
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse

from services.models import Service
from .models import Barber, Reservation
from reservation.models import BarberBlockedTime


# =========================================================
# صفحه رزرو
# =========================================================

@login_required(login_url="/login/")
def reservation_view(request):

    services = Service.objects.filter(
        is_active=True
    ).order_by("order")

    barbers = Barber.objects.filter(
        is_active=True
    )

    if request.method == "POST":

        service_id = request.POST.get("service")
        barber_id = request.POST.get("barber")
        date_str = request.POST.get("date")
        time_str = request.POST.get("time")

        # -----------------------------
        # بررسی اطلاعات
        # -----------------------------

        if not all([
            service_id,
            barber_id,
            date_str,
            time_str
        ]):

            messages.error(
                request,
                "لطفاً تمام اطلاعات را تکمیل کنید."
            )

            return redirect("reservation")

        # -----------------------------
        # دریافت اطلاعات
        # -----------------------------

        try:

            service = Service.objects.get(
                id=service_id,
                is_active=True
            )

            barber = Barber.objects.get(
                id=barber_id,
                is_active=True
            )

            date = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()

            time = datetime.strptime(
                time_str,
                "%H:%M"
            ).time()

        except Exception as e:

            print(e)

            messages.error(
                request,
                "اطلاعات وارد شده صحیح نیست."
            )

            return redirect("reservation")

        # -----------------------------
        # بررسی رزرو قبلی
        # -----------------------------

        reservation_exists = Reservation.objects.filter(
            barber=barber,
            date=date,
            time=time
        ).exclude(
            status="cancel"
        ).exists()

        # -----------------------------
        # بررسی زمان مسدود
        # -----------------------------

        blocked_exists = BarberBlockedTime.objects.filter(
            barber=barber,
            date=date,
            start_time__lte=time,
            end_time__gt=time
        ).exists()

        if reservation_exists or blocked_exists:

            messages.error(
                request,
                "این ساعت در دسترس نیست."
            )

            return redirect("reservation")

        # -----------------------------
        # محاسبه مبلغ
        # -----------------------------

        service_price = service.price

        # 10 درصد بیعانه
        deposit_amount = int(
            service_price * 10 / 100
        )

        # -----------------------------
        # ایجاد رزرو
        # -----------------------------

        reservation = Reservation.objects.create(

            user=request.user,

            customer_name=request.user.full_name,

            customer_phone=request.user.phone,

            service=service,

            barber=barber,

            date=date,

            time=time,

            service_price=service_price,

            deposit_amount=deposit_amount,

            status="pending",

            payment_status="pending",
        )

        # -----------------------------
        # انتقال به صفحه پرداخت
        # -----------------------------

        return redirect(
            "reservation_payment",
            reservation_id=reservation.id
        )

    # -----------------------------
    # نمایش صفحه رزرو
    # -----------------------------

    return render(
        request,
        "core/reservation.html",
        {
            "services": services,
            "barbers": barbers,
        }
    )


# =========================================================
# API ساعت‌های مسدود
# =========================================================

@login_required
def blocked_times_api(request):

    barber_id = request.GET.get("barber")
    date = request.GET.get("date")

    barber = get_object_or_404(
        Barber,
        id=barber_id,
        is_active=True
    )

    blocked = BarberBlockedTime.objects.filter(
        barber=barber,
        date=date
    )

    reservations = Reservation.objects.filter(
        barber=barber,
        date=date
    ).exclude(
        status="cancel"
    )

    data = []

    # -----------------------------
    # ساعت کاری آرایشگر
    # -----------------------------

    data.append({
        "type": "working_hours",

        "start": barber.work_start.strftime("%H:%M"),

        "end": barber.work_end.strftime("%H:%M"),

        "duration": barber.appointment_duration,
    })

    # -----------------------------
    # ساعت‌های مسدود
    # -----------------------------

    for item in blocked:

        data.append({

            "type": "blocked",

            "start": item.start_time.strftime("%H:%M"),

            "end": item.end_time.strftime("%H:%M"),
        })

    # -----------------------------
    # نوبت‌های رزرو شده
    # -----------------------------

    for item in reservations:

        start_minutes = (
            item.time.hour * 60
            + item.time.minute
        )

        end_minutes = (
            start_minutes
            + barber.appointment_duration
        )

        end_hour = end_minutes // 60

        end_minute = end_minutes % 60

        data.append({

            "type": "blocked",

            "start": item.time.strftime("%H:%M"),

            "end": f"{end_hour:02d}:{end_minute:02d}",
        })

    return JsonResponse(
        data,
        safe=False
    )


# =========================================================
# ساعت کاری آرایشگر
# =========================================================

@login_required
def barber_working_hours(request):

    barber_id = request.GET.get("barber")

    if not barber_id:

        return JsonResponse({

            "work_start": "09:00",

            "work_end": "18:00",

            "appointment_duration": 30
        })

    try:

        barber = Barber.objects.get(
            id=barber_id,
            is_active=True
        )

    except Barber.DoesNotExist:

        return JsonResponse(
            {
                "error": "barber not found"
            },
            status=404
        )

    return JsonResponse({

        "work_start": barber.work_start.strftime("%H:%M"),

        "work_end": barber.work_end.strftime("%H:%M"),

        "appointment_duration": barber.appointment_duration
    })


# =========================================================
# لغو رزرو
# =========================================================

@login_required
def cancel_reservation(request, id):

    reservation = get_object_or_404(

        Reservation,

        id=id,

        user=request.user
    )

    if reservation.status in [
        "pending",
        "approved"
    ]:

        reservation.status = "cancel"

        reservation.save()

    return redirect("/profile/")


# =========================================================
# صفحه پرداخت بیعانه
# =========================================================

@login_required(login_url="/login/")
def reservation_payment(request, reservation_id):

    reservation = get_object_or_404(

        Reservation,

        id=reservation_id,

        user=request.user
    )

    # اگر قبلاً پرداخت شده
    if reservation.payment_status == "paid":

        messages.info(
            request,
            "بیعانه این نوبت قبلاً پرداخت شده است."
        )

        return redirect("/profile/")

    # اگر رزرو لغو شده
    if reservation.status == "cancel":

        messages.error(
            request,
            "این نوبت لغو شده است."
        )

        return redirect("/profile/")

    return render(

        request,

        "core/reservation_payment.html",

        {
            "reservation": reservation
        }
    )

