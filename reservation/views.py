from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from discounts.models import DiscountCode, DiscountUsage

from services.models import Service, BarberServicePrice
from .models import Barber, Reservation
from reservation.models import BarberBlockedTime
from users.sms import send_appointment_confirmation_sms

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
            "barber_prices",
            "details__barber_prices",
        )
    )

    barbers = Barber.objects.filter(
        is_active=True
    )

    # =====================================================
    # ثبت اطلاعات رزرو
    # =====================================================

    if request.method == "POST":

        service_ids = request.POST.getlist("services")

        if not service_ids:

            messages.error(
                request,
                "حداقل یک خدمت را انتخاب کنید."
            )

            return redirect("reservation")

        service_ids = list(
            dict.fromkeys(service_ids)
        )

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
            # جزئیات انتخاب‌شده خدمت
            # =================================================

            selected_detail_ids = request.POST.getlist(
                f"details_{service_id}"
            )

            selected_details = []

            details_price = 0

            details_duration = 0

            for detail_id in selected_detail_ids:

                detail = (
                    service.details
                    .filter(
                        id=detail_id,
                        is_active=True
                    )
                    .first()
                )

                if not detail:

                    messages.error(
                        request,
                        "یکی از جزئیات انتخاب‌شده معتبر نیست."
                    )

                    return redirect("reservation")

                barber_detail_price = (
                    detail.barber_prices
                    .filter(
                        barber=barber
                    )
                    .first()
                )

                if not barber_detail_price:

                    messages.error(
                        request,
                        f"جزئیات «{detail.name}» برای این آرایشگر ثبت نشده است."
                    )

                    return redirect("reservation")

                details_price += (
                    barber_detail_price.price
                )

                details_duration += (
                    barber_detail_price.duration
                )

                selected_details.append({

                    "id": detail.id,

                    "name": detail.name,

                    "price": int(
                        barber_detail_price.price
                    ),

                    "duration": int(
                        barber_detail_price.duration
                    ),

                })

            # =================================================
            # مبلغ و مدت نهایی
            # =================================================

            total_service_price = (
                service_price
                + details_price
            )

            total_duration = (
                appointment_duration
                + details_duration
            )

            # =================================================
            # زمان شروع و پایان
            # =================================================

            start_datetime = datetime.combine(
                date,
                time
            )

            end_datetime = (
                start_datetime
                + timedelta(
                    minutes=total_duration
                )
            )

            # =================================================
            # بررسی ساعت کاری
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
            # بررسی روز کاری
            # =================================================

            weekday = (
                date.weekday() + 2
            ) % 7

            working_day = (
                barber.working_days
                .filter(
                    day=weekday,
                    is_working=True
                )
                .exists()
            )

            if not working_day:

                messages.error(
                    request,
                    f"{barber.user.full_name} در این روز کاری ندارد."
                )

                return redirect("reservation")

            # =================================================
            # بررسی روز تعطیل
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
            # بررسی تداخل با رزروهای واقعی قبلی
            # =================================================

            existing_reservations = (
                Reservation.objects
                .filter(
                    barber=barber,
                    date=date
                )
                .exclude(
                    status__in=[
                        "cancel",
                        "draft"
                    ]
                )
            )

            reservation_conflict = False

            for existing in existing_reservations:

                existing_start = datetime.combine(
                    existing.date,
                    existing.time
                )

                existing_duration = (
                    existing.total_duration
                )

                if not existing_duration:

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
            # بررسی تداخل خدمات انتخاب‌شده همین فرم
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
                            minutes=item["total_duration"]
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
                total_service_price * 10 / 100
            )

            # =================================================
            # ذخیره موقت در حافظه
            # =================================================

            reservations_data.append({

                "service": service,

                "barber": barber,

                "date": date,

                "time": time,

                "appointment_duration":
                    total_duration,

                "service_price":
                    total_service_price,

                "deposit_amount":
                    deposit_amount,

                "selected_details":
                    selected_details,

                "total_duration":
                    total_duration,

            })

        # =====================================================
        # ذخیره موقت اطلاعات در Session
        # =====================================================

        pending_reservations = []

        for item in reservations_data:

            pending_reservations.append({

                "service_id":
                    item["service"].id,

                "barber_id":
                    item["barber"].id,

                "date":
                    item["date"].isoformat(),

                "time":
                    item["time"].strftime("%H:%M"),

                "service_price":
                    int(item["service_price"]),

                "deposit_amount":
                    int(item["deposit_amount"]),

                "selected_details":
                    item["selected_details"],

                "total_duration":
                    int(item["total_duration"]),

            })

        request.session[
            "pending_reservations"
        ] = pending_reservations

        # =====================================================
        # پاک کردن انتخاب‌های قبلی
        # =====================================================

        request.session.pop(
            "reservation_discount_code",
            None
        )

        request.session.pop(
            "reservation_discount_amount",
            None
        )

        request.session.pop(
            "selected_payment_type",
            None
        )

        request.session.pop(
            "selected_payment_amount",
            None
        )

        request.session.modified = True

        # =====================================================
        # انتقال به صفحه پرداخت
        # =====================================================

        return redirect(
            "reservation_payment"
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
              status__in=["cancel", "draft"]
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

        reservation_duration = item.total_duration

        if not reservation_duration:
             reservation_duration = barber.appointment_duration

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
def reservation_payment(request):

    # =====================================================
    # دریافت اطلاعات موقت از Session
    # =====================================================

    pending_reservations = request.session.get(
        "pending_reservations"
    )

    if not pending_reservations:

        messages.error(
            request,
            "اطلاعات رزرو پیدا نشد. دوباره تلاش کنید."
        )

        return redirect("reservation")

    # =====================================================
    # ساخت اطلاعات رزرو برای نمایش صفحه
    # =====================================================

    reservations_data = []

    base_total_price = 0

    for item in pending_reservations:

        try:

            service = Service.objects.get(
                id=item["service_id"],
                is_active=True
            )

            barber = Barber.objects.get(
                id=item["barber_id"],
                is_active=True
            )

            date = datetime.strptime(
                item["date"],
                "%Y-%m-%d"
            ).date()

            time = datetime.strptime(
                item["time"],
                "%H:%M"
            ).time()

        except (
            Service.DoesNotExist,
            Barber.DoesNotExist,
            ValueError
        ):

            messages.error(
                request,
                "اطلاعات یکی از رزروها دیگر معتبر نیست."
            )

            request.session.pop(
                "pending_reservations",
                None
            )

            request.session.modified = True

            return redirect("reservation")

        reservations_data.append({

            "service": service,

            "barber": barber,

            "date": date,

            "time": time,

            "service_price":
                int(item["service_price"]),

            "deposit_amount":
                int(item["deposit_amount"]),

            "selected_details":
                item.get(
                    "selected_details",
                    []
                ),

            "total_duration":
                int(
                    item["total_duration"]
                ),

        })

        base_total_price += int(
            item["service_price"]
        )

    # =====================================================
    # اطلاعات تخفیف
    # =====================================================

    discount_code = request.session.get(
        "reservation_discount_code"
    )

    discount_amount = int(
        request.session.get(
            "reservation_discount_amount",
            0
        )
    )

    discount_error = None
    discount_success = None

    total_price = base_total_price

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        # =================================================
        # اعمال کد تخفیف
        # =================================================

        code = request.POST.get(
            "discount_code"
        )

        if code is not None:

            code = code.strip().upper()

            request.session.pop(
                "reservation_discount_code",
                None
            )

            request.session.pop(
                "reservation_discount_amount",
                None
            )

            discount_code = None
            discount_amount = 0

            if not code:

                discount_error = (
                    "کد تخفیف را وارد کنید."
                )

            else:

                try:

                    discount = DiscountCode.objects.get(
                        code=code
                    )

                except DiscountCode.DoesNotExist:

                    discount_error = (
                        "کد تخفیف وارد شده معتبر نیست."
                    )

                else:

                    if not discount.is_valid_now():

                        discount_error = (
                            "این کد تخفیف فعال یا معتبر نیست."
                        )

                    else:

                        user_usage_count = (
                            DiscountUsage.objects
                            .filter(
                                discount=discount,
                                user=request.user
                            )
                            .count()
                        )

                        if (
                            discount.per_user_limit is not None
                            and user_usage_count
                            >= discount.per_user_limit
                        ):

                            discount_error = (
                                "شما قبلاً به تعداد مجاز "
                                "از این کد استفاده کرده‌اید."
                            )

                        elif (
                            discount.users.exists()
                            and not discount.users.filter(
                                id=request.user.id
                            ).exists()
                        ):

                            discount_error = (
                                "این کد تخفیف برای حساب "
                                "شما قابل استفاده نیست."
                            )

                        elif (
                            discount.minimum_purchase
                            and base_total_price
                            < discount.minimum_purchase
                        ):

                            discount_error = (
                                f"حداقل مبلغ خرید برای این کد "
                                f"{discount.minimum_purchase:,} تومان است."
                            )

                        else:

                            eligible_reservations = []

                            if discount.services_all:

                                eligible_reservations = (
                                    reservations_data
                                )

                            else:

                                for item in reservations_data:

                                    if discount.services.filter(
                                        id=item["service"].id
                                    ).exists():

                                        eligible_reservations.append(
                                            item
                                        )

                            if not eligible_reservations:

                                discount_error = (
                                    "این کد تخفیف برای "
                                    "خدمات انتخاب‌شده قابل استفاده نیست."
                                )

                            else:

                                eligible_amount = sum(
                                    item["service_price"]
                                    for item
                                    in eligible_reservations
                                )

                                if (
                                    discount.discount_type
                                    == "percent"
                                ):

                                    discount_amount = (
                                        eligible_amount
                                        * discount.value
                                        // 100
                                    )

                                else:

                                    discount_amount = min(
                                        discount.value,
                                        eligible_amount
                                    )

                                total_price = max(
                                    base_total_price
                                    - discount_amount,
                                    0
                                )

                                request.session[
                                    "reservation_discount_code"
                                ] = discount.code

                                request.session[
                                    "reservation_discount_amount"
                                ] = int(
                                    discount_amount
                                )

                                discount_code = discount.code

                                discount_success = (
                                    "کد تخفیف با موفقیت اعمال شد."
                                )

                                request.session.modified = True

        # =================================================
        # پرداخت
        # =================================================

        else:

            payment_type = request.POST.get(
                "payment_type"
            )

            if payment_type not in [
                "deposit",
                "full"
            ]:

                messages.error(
                    request,
                    "نوع پرداخت نامعتبر است."
                )

                return redirect(
                    "reservation_payment"
                )

            # =================================================
            # محاسبه مبلغ
            # =================================================

            total_deposit = int(
                total_price * 10 / 100
            )

            if payment_type == "deposit":

                payable_amount = total_deposit

            else:

                payable_amount = total_price

            # =================================================
            # جلوگیری از دوباره ساخته شدن رزرو
            # =================================================

            existing_ids = request.session.get(
                "created_reservation_ids"
            )

            if existing_ids:

                existing_count = (
                    Reservation.objects
                    .filter(
                        id__in=existing_ids,
                        user=request.user
                    )
                    .count()
                )

                if existing_count == len(existing_ids):

                    request.session[
                        "selected_payment_type"
                    ] = payment_type

                    request.session[
                        "selected_payment_amount"
                    ] = payable_amount

                    request.session.modified = True

                    return redirect(
                        "reservation_payment"
                    )

            # =================================================
            # ساخت واقعی رزروها
            # =================================================

            created_reservation_ids = []

            try:

                with transaction.atomic():

                    for item in reservations_data:

                        reservation = (
                            Reservation.objects.create(

                                user=request.user,

                                customer_name=(
                                    request.user.full_name
                                ),

                                customer_phone=(
                                    request.user.phone
                                ),

                                service=item["service"],

                                barber=item["barber"],

                                date=item["date"],

                                time=item["time"],

                                service_price=(
                                    item["service_price"]
                                ),

                                deposit_amount=int(
                                    total_price * 10 / 100
                                ),

                                selected_details=(
                                    item["selected_details"]
                                ),

                                total_duration=(
                                    item["total_duration"]
                                ),

                                status="pending",

                                payment_status="pending",
                            )
                        )

                        created_reservation_ids.append(
                            reservation.id
                        )

                        # =====================================
                        # پیامک فقط بعد از ایجاد رزرو
                        # =====================================

                        send_appointment_confirmation_sms(

                            phone=request.user.phone,

                            name=request.user.full_name,

                            barber=(
                                reservation
                                .barber
                                .user
                                .full_name
                            ),

                            date=reservation.date,

                            appointment_time=(
                                reservation.time
                            ),

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

                return redirect(
                    "reservation_payment"
                )

            # =================================================
            # ذخیره ID رزروهای واقعی
            # =================================================

            request.session[
                "created_reservation_ids"
            ] = created_reservation_ids

            request.session[
                "selected_payment_type"
            ] = payment_type

            request.session[
                "selected_payment_amount"
            ] = payable_amount

            # اطلاعات موقت دیگر لازم نیست

            request.session.pop(
                "pending_reservations",
                None
            )

            request.session.modified = True

            # =================================================
            # اینجا بعداً اتصال درگاه پرداخت
            # =================================================

            messages.success(
                request,
                (
                    "رزرو با موفقیت ثبت شد. "
                    "در حال انتقال به پرداخت..."
                )
            )

            return redirect(
                "reservation_payment"
            )

    # =====================================================
    # تخفیف قبلی Session
    # =====================================================

    elif discount_code:

        try:

            discount = DiscountCode.objects.get(
                code=discount_code
            )

            if discount.is_valid_now():

                discount_amount = min(
                    discount_amount,
                    base_total_price
                )

                total_price = max(
                    base_total_price
                    - discount_amount,
                    0
                )

            else:

                request.session.pop(
                    "reservation_discount_code",
                    None
                )

                request.session.pop(
                    "reservation_discount_amount",
                    None
                )

                discount_code = None
                discount_amount = 0

                request.session.modified = True

        except DiscountCode.DoesNotExist:

            request.session.pop(
                "reservation_discount_code",
                None
            )

            request.session.pop(
                "reservation_discount_amount",
                None
            )

            discount_code = None
            discount_amount = 0

            request.session.modified = True

    # =====================================================
    # بیعانه
    # =====================================================

    total_deposit = int(
        total_price * 10 / 100
    )

    # =====================================================
    # انتخاب قبلی پرداخت
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
    # رزروهای واقعی ساخته‌شده
    # برای نمایش در صفحه
    # =====================================================

    created_reservation_ids = request.session.get(
        "created_reservation_ids",
        []
    )

    real_reservations = (
        Reservation.objects
        .filter(
            id__in=created_reservation_ids,
            user=request.user
        )
        .order_by(
            "date",
            "time"
        )
    )

    # =====================================================
    # نمایش صفحه
    # =====================================================

    return render(
        request,
        "core/reservation_payment.html",
        {
            "reservation":
                real_reservations.first(),

            "reservations":
                real_reservations,

            "reservations_data":
                reservations_data,

            "base_total_price":
                base_total_price,

            "total_price":
                total_price,

            "total_deposit":
                total_deposit,

            "discount_code":
                discount_code,

            "discount_amount":
                discount_amount,

            "discount_error":
                discount_error,

            "discount_success":
                discount_success,

            "selected_payment_type":
                selected_payment_type,

            "selected_payment_amount":
                selected_payment_amount,
        }
    )