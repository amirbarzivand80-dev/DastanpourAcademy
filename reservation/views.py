from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from services.models import Service
from .models import Barber, Reservation
from reservation.models import BarberBlockedTime
from django.http import JsonResponse
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

        if not all([service_id, barber_id, date_str, time_str]):
            messages.error(
                request,
                "لطفاً تمام اطلاعات را تکمیل کنید."
            )
            return redirect("reservation")

        try:

            service = Service.objects.get(id=service_id)
            barber = Barber.objects.get(id=barber_id)

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
            raise

        reservation_exists = Reservation.objects.filter(
            barber=barber,
            date=date,
            time=time
        ).exists()

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

        Reservation.objects.create(
            user=request.user,
            service=service,
            barber=barber,
            date=date,
            time=time
        )

        messages.success(
            request,
            "رزرو شما با موفقیت ثبت شد."
        )

        return redirect("reservation")

    return render(
        request,
        "core/reservation.html",
        {
            "services": services,
            "barbers": barbers,
        }
    )
@login_required
def blocked_times_api(request):

    barber_id = request.GET.get("barber")
    date = request.GET.get("date")

    blocked = BarberBlockedTime.objects.filter(
        barber_id=barber_id,
        date=date
    )

    reservations = Reservation.objects.filter(
        barber_id=barber_id,
        date=date
    )

    data = []

    # ساعت‌های مسدود
    for item in blocked:

        data.append({

            "start": item.start_time.strftime("%H:%M"),
            "end": item.end_time.strftime("%H:%M"),

        })

    # ساعت‌های رزرو شده
    for item in reservations:

        start = item.time.strftime("%H:%M")

        end_hour = item.time.hour
        end_minute = item.time.minute + 30

        if end_minute >= 60:
            end_hour += 1
            end_minute -= 60

        end = f"{end_hour:02d}:{end_minute:02d}"

        data.append({

            "start": start,
            "end": end,

        })

    return JsonResponse(data, safe=False)

from django.shortcuts import get_object_or_404


@login_required
def cancel_reservation(request, id):

    reservation = get_object_or_404(

        Reservation,

        id=id,

        user=request.user

    )

    if reservation.status in ["pending", "approved"]:

        reservation.status = "cancel"

        reservation.save()

    return redirect("/profile/")