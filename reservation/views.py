from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse

from services.models import Service, BarberServicePrice
from .models import Barber, Reservation
from reservation.models import BarberBlockedTime


# =========================================================
# صفحه رزرو
# =========================================================
@login_required(login_url="/login/")
def reservation_view(request):

    services = (
        Service.objects
        .filter(is_active=True)
        .order_by("order")
        .prefetch_related(
            "barbers",
            "barber_prices"
        )
    )

    barbers = Barber.objects.filter(
        is_active=True
    )

    # =====================================================
    # ثبت رزرو
    # =====================================================

    if request.method == "POST":

        service_ids = request.POST.getlist("services")

        if not service_ids:

            messages.error(
                request,
                "حداقل یک خدمت را انتخاب کنید."
            )

            return redirect("reservation")

        service_ids = list(dict.fromkeys(service_ids))

        reservations_data = []

        # =================================================
        # بررسی تک تک خدمات
        # =================================================

        for service_id in service_ids:

            barber_id = request.POST.get(
                f"barber_{service_id}"
            )

            date_str = request.POST.get(
                f"date_{service_id}"
            )

            time_str = request.POST.get(
                f"time_{service_id}"
            )

            if not all([
                barber_id,
                date_str,
                time_str
            ]):

                messages.error(
                    request,
                    "لطفاً آرایشگر، تاریخ و ساعت همه خدمات انتخاب‌شده را مشخص کنید."
                )

                return redirect("reservation")

            # =================================================
            # دریافت اطلاعات
            # =================================================

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

            except (
                Service.DoesNotExist,
                Barber.DoesNotExist,
                ValueError
            ):

                messages.error(
                    request,
                    "اطلاعات یکی از خدمات صحیح نیست."
                )

                return redirect("reservation")

            # =================================================
            # بررسی ارائه خدمت توسط آرایشگر
            # =================================================

            if not service.barbers.filter(
                id=barber.id
            ).exists():

                messages.error(
                    request,
                    f"آرایشگر انتخاب‌شده خدمت «{service.name}» را ارائه نمی‌دهد."
                )

                return redirect("reservation")

            # =================================================
            # قیمت و مدت اختصاصی آرایشگر
            # =================================================

            barber_price = (
                BarberServicePrice.objects
                .filter(
                    service=service,
                    barber=barber
                )
                .first()
            )

            if not barber_price:

                messages.error(
                    request,
                    f"قیمت و مدت خدمت «{service.name}» برای این آرایشگر ثبت نشده است."
                )

                return redirect("reservation")

            service_price = barber_price.price

            appointment_duration = barber_price.duration

            # =================================================
            # محاسبه زمان پایان
            # =================================================

            start_datetime = datetime.combine(
                date,
                time
            )

            end_datetime = (
                start_datetime
                + timedelta(
                    minutes=appointment_duration
                )
            )

            # =================================================
            # بررسی ساعت کاری آرایشگر
            # =================================================

            work_start = datetime.combine(
                date,
                barber.work_start
            )

            work_end = datetime.combine(
                date,
                barber.work_end
            )

            if (
                start_datetime < work_start
                or end_datetime > work_end
            ):

                messages.error(
                    request,
                    f"ساعت انتخاب‌شده خارج از ساعت کاری "
                    f"{barber.user.full_name} است."
                )

                return redirect("reservation")

            # =================================================
            # بررسی روز کاری آرایشگر
            # =================================================

            weekday = (date.weekday() + 2) % 7

            working_day = barber.working_days.filter(
                day=weekday,
                is_working=True
            ).exists()

            if not working_day:

                messages.error(
                    request,
                    f"{barber.user.full_name} در این روز کاری ندارد."
                )

                return redirect("reservation")

            # =================================================
            # بررسی روز تعطیل آرایشگر
            # =================================================

            if barber.days_off.filter(
                date=date
            ).exists():

                messages.error(
                    request,
                    f"{barber.user.full_name} در این تاریخ تعطیل است."
                )

                return redirect("reservation")

            # =================================================
            # بررسی تداخل با رزروهای قبلی
            # =================================================

            existing_reservations = (
                Reservation.objects
                .filter(
                    barber=barber,
                    date=date
                )
                .exclude(
                    status="cancel"
                )
                .select_related(
                    "service"
                )
            )

            reservation_conflict = False

            for existing in existing_reservations:

                existing_start = datetime.combine(
                    existing.date,
                    existing.time
                )

                existing_price = (
                    BarberServicePrice.objects
                    .filter(
                        barber=barber,
                        service=existing.service
                    )
                    .first()
                )

                if existing_price:

                    existing_duration = (
                        existing_price.duration
                    )

                else:

                    existing_duration = (
                        barber.appointment_duration
                    )

                existing_end = (
                    existing_start
                    + timedelta(
                        minutes=existing_duration
                    )
                )

                if (
                    start_datetime < existing_end
                    and end_datetime > existing_start
                ):

                    reservation_conflict = True
                    break

            if reservation_conflict:

                messages.error(
                    request,
                    f"ساعت {time.strftime('%H:%M')} "
                    f"برای {barber.user.full_name} "
                    f"در خدمت «{service.name}» در دسترس نیست."
                )

                return redirect("reservation")

            # =================================================
            # بررسی زمان‌های مسدود
            # =================================================

            blocked_times = (
                BarberBlockedTime.objects
                .filter(
                    barber=barber,
                    date=date
                )
            )

            blocked_conflict = False

            for blocked in blocked_times:

                blocked_start = datetime.combine(
                    blocked.date,
                    blocked.start_time
                )

                blocked_end = datetime.combine(
                    blocked.date,
                    blocked.end_time
                )

                if (
                    start_datetime < blocked_end
                    and end_datetime > blocked_start
                ):

                    blocked_conflict = True
                    break

            if blocked_conflict:

                messages.error(
                    request,
                    f"ساعت انتخاب‌شده برای "
                    f"{barber.user.full_name} "
                    f"در خدمت «{service.name}» مسدود است."
                )

                return redirect("reservation")

            # =================================================
            # بررسی تداخل خدمات همین فرم
            # =================================================

            for item in reservations_data:

                if (
                    item["barber"].id == barber.id
                    and item["date"] == date
                ):

                    selected_start = datetime.combine(
                        item["date"],
                        item["time"]
                    )

                    selected_end = (
                        selected_start
                        + timedelta(
                            minutes=item["appointment_duration"]
                        )
                    )

                    if (
                        start_datetime < selected_end
                        and end_datetime > selected_start
                    ):

                        messages.error(
                            request,
                            f"دو خدمت انتخاب‌شده برای "
                            f"{barber.user.full_name} "
                            f"با هم تداخل زمانی دارند."
                        )

                        return redirect("reservation")

            # =================================================
            # بیعانه
            # =================================================

            deposit_amount = int(
                service_price * 10 / 100
            )

            # =================================================
            # ذخیره اطلاعات خدمت
            # =================================================

            reservations_data.append({

                "service": service,

                "barber": barber,

                "date": date,

                "time": time,

                "appointment_duration":
                    appointment_duration,

                "service_price":
                    service_price,

                "deposit_amount":
                    deposit_amount,

            })

        # =====================================================
        # ساخت تمام رزروها
        # =====================================================

        created_reservation_ids = []

        try:

            with transaction.atomic():

                for item in reservations_data:

                    reservation = Reservation.objects.create(

                        user=request.user,

                        customer_name=request.user.full_name,

                        customer_phone=request.user.phone,

                        service=item["service"],

                        barber=item["barber"],

                        date=item["date"],

                        time=item["time"],

                        service_price=item["service_price"],

                        deposit_amount=item["deposit_amount"],

                        status="pending",

                        payment_status="pending",
                    )

                    created_reservation_ids.append(
                        reservation.id
                    )

        except Exception as e:

            print(
                "RESERVATION CREATE ERROR:",
                e
            )

            messages.error(
                request,
                "ثبت رزروها با خطا مواجه شد. دوباره تلاش کنید."
            )

            return redirect("reservation")

        # =====================================================
        # ذخیره رزروهای این فرآیند
        # =====================================================

        request.session[
            "pending_reservation_ids"
        ] = created_reservation_ids

        request.session.pop(
            "pending_payment_type",
            None
        )

        request.session.pop(
            "pending_payment_amount",
            None
        )

        request.session.modified = True

        # =====================================================
        # انتقال به صفحه پرداخت
        # =====================================================

        return redirect(
            "reservation_payment",
            reservation_id=created_reservation_ids[-1]
        )

    # =====================================================
    # نمایش صفحه رزرو
    # =====================================================

    return render(
        request,
        "core/reservation.html",
        {
            "services": services,
            "barbers": barbers,
        }
    )

# =========================================================
# API ساعت‌های مسدود / رزرو شده
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

    reservations = (
        Reservation.objects
        .filter(
            barber=barber,
            date=date
        )
        .exclude(
            status="cancel"
        )
        .select_related(
            "service"
        )
    )

    data = []

    # =====================================================
    # ساعت کاری
    # =====================================================

    data.append({

        "type": "working_hours",

        "start":
            barber.work_start.strftime("%H:%M"),

        "end":
            barber.work_end.strftime("%H:%M"),

        "duration":
            barber.appointment_duration,

    })

    # =====================================================
    # زمان‌های مسدود
    # =====================================================

    for item in blocked:

        data.append({

            "type": "blocked",

            "start":
                item.start_time.strftime("%H:%M"),

            "end":
                item.end_time.strftime("%H:%M"),

        })

    # =====================================================
    # رزروهای قبلی
    # =====================================================

    for item in reservations:

        start_minutes = (
            item.time.hour * 60
            + item.time.minute
        )

        # مدت اختصاصی همین خدمت
        barber_service_price = (
            BarberServicePrice.objects
            .filter(
                barber=barber,
                service=item.service
            )
            .first()
        )

        if barber_service_price:

            reservation_duration = (
                barber_service_price.duration
            )

        else:

            reservation_duration = (
                barber.appointment_duration
            )

        end_minutes = (
            start_minutes
            + reservation_duration
        )

        end_hour = end_minutes // 60

        end_minute = end_minutes % 60

        data.append({

            "type": "blocked",

            "start":
                item.time.strftime("%H:%M"),

            "end":
                f"{end_hour:02d}:{end_minute:02d}",

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

        "work_start":
            barber.work_start.strftime("%H:%M"),

        "work_end":
            barber.work_end.strftime("%H:%M"),

        "appointment_duration":
            barber.appointment_duration

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
# صفحه پرداخت
# =========================================================
@login_required(login_url="/login/")
def reservation_payment(request, reservation_id):

    # =====================================================
    # رزرو اصلی
    # =====================================================

    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    # =====================================================
    # دریافت تمام رزروهای این فرآیند
    # =====================================================

    reservation_ids = request.session.get(
        "pending_reservation_ids"
    )

    if not reservation_ids:
        reservation_ids = [reservation.id]

    reservations = (
        Reservation.objects
        .filter(
            id__in=reservation_ids,
            user=request.user
        )
        .exclude(
            status="cancel"
        )
        .order_by(
            "date",
            "time"
        )
    )

    # =====================================================
    # بررسی وجود رزرو
    # =====================================================

    if not reservations.exists():

        messages.error(
            request,
            "هیچ رزرو فعالی برای پرداخت وجود ندارد."
        )

        request.session.pop(
            "pending_reservation_ids",
            None
        )

        return redirect("/profile/")

    # =====================================================
    # محاسبه مبالغ
    # =====================================================

    total_price = sum(
        item.service_price
        for item in reservations
    )

    total_deposit = sum(
        item.deposit_amount
        for item in reservations
    )

    # =====================================================
    # اگر فرم پرداخت ارسال شده
    # =====================================================

    if request.method == "POST":

        payment_type = request.POST.get(
            "payment_type"
        )

        # -------------------------------------------------
        # اعتبارسنجی نوع پرداخت
        # -------------------------------------------------

        if payment_type not in [
            "deposit",
            "full"
        ]:

            messages.error(
                request,
                "نوع پرداخت نامعتبر است."
            )

            return redirect(
                "reservation_payment",
                reservation_id=reservation.id
            )

        # -------------------------------------------------
        # تعیین مبلغ قابل پرداخت
        # -------------------------------------------------

        if payment_type == "deposit":

            payable_amount = total_deposit

        else:

            payable_amount = total_price

        # =================================================
        # فعلاً درگاه نداریم
        #
        # بنابراین انتخاب کاربر را در Session نگه می‌داریم.
        # بعداً همین payable_amount را می‌دهیم به درگاه.
        # =================================================

        request.session[
            "selected_payment_type"
        ] = payment_type

        request.session[
            "selected_payment_amount"
        ] = payable_amount

        request.session.modified = True

        # -------------------------------------------------
        # فعلاً برگرد به همین صفحه
        # -------------------------------------------------

        messages.success(
            request,
            (
                "پرداخت بیعانه انتخاب شد."
                if payment_type == "deposit"
                else
                "پرداخت کامل انتخاب شد."
            )
        )

        return redirect(
            "reservation_payment",
            reservation_id=reservation.id
        )

    # =====================================================
    # انتخاب قبلی کاربر
    # =====================================================

    selected_payment_type = request.session.get(
        "selected_payment_type",
        "deposit"
    )

    selected_payment_amount = request.session.get(
        "selected_payment_amount",
        total_deposit
    )

    # =====================================================
    # نمایش صفحه
    # =====================================================

    return render(
        request,
        "core/reservation_payment.html",
        {
            "reservation": reservation,

            "reservations": reservations,

            "total_price": total_price,

            "total_deposit": total_deposit,

            "selected_payment_type":
                selected_payment_type,

            "selected_payment_amount":
                selected_payment_amount,
        }
    )