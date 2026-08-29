from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from core.models import HomeOffer
from users.models import CustomUser
from reservation.models import Reservation, Barber
from services.models import Service
from django.utils import timezone
import jdatetime
from datetime import datetime
import jdatetime
from users.models import  CustomerGalleryImage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .forms import UserEditForm, BarberForm
from reservation.models import Barber
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from services.models import Service, BarberServicePrice
from services.forms import ServiceForm
from .models import AdminPermission
from .forms import AdminPermissionForm
from .decorators import permission_required
from reservation.models import BarberBlockedTime
from reservation.forms import BarberBlockedTimeForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from reservation.forms import WalkInReservationForm
from users.models import CustomUser
from academy.models import Course
from academy.forms import CourseForm
from users.sms import send_survey_sms
from academy.models import CourseStudent
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from users.sms import send_order_confirmation_sms
from academy.models import Course, CourseStudent
from academy.models import Course, CourseStudent,CourseSession,CourseFeature
from django.shortcuts import get_object_or_404, render
from academy.models import CourseTopic
from reservation.models import Barber, BarberWorkingDay
from academy.models import CourseImage
from services.models import (
    Service,
    ServiceImage,
    BarberServicePrice,
    ServiceDetail,
    BarberServiceDetailPrice,
)
from .forms import BarberForm, BarberEditForm
@login_required
def dashboard(request):

    # اگر سوپرادمین باشد داشبورد کامل را ببیند
    if request.user.is_super_admin:

        context = {

         "users_count": CustomUser.objects.count(),

         "barbers_count": Barber.objects.count(),

        "services_count": Service.objects.count(),

       "reservation_count": Reservation.objects.count(),

         "products_count": Product.objects.count(),

        "orders_count": Order.objects.count(),

       "last_reservations": Reservation.objects.select_related(
        "user",
        "barber",
        "service"
      ).order_by("-created_at")[:8],

         "last_orders": Order.objects.select_related(
        "user"
      ).order_by("-created_at")[:5],

     "last_messages": ContactMessage.objects.order_by(
        "-created_at"
    )[:5],

     "pending_comments": ProductComment.objects.filter(
        is_active=False
      ).select_related(
        "user",
        "product"
      ).order_by("-created_at")[:5],

}

        return render(
            request,
            "superadmin_panel/dashboard.html",
            context
        )

    # اگر آرایشگر باشد
    if request.user.is_barber:
        return redirect("superadmin_reservations")

    # اگر مدیر باشد
    if hasattr(request.user, "admin_permission"):

        p = request.user.admin_permission

        if p.users_access:
            return redirect("superadmin_users")

        if p.barbers_access:
            return redirect("superadmin_barbers")

        if p.services_access:
            return redirect("superadmin_services")

        if p.reservations_access:
            return redirect("superadmin_reservations")

    # اگر هیچکدام نبود
    return redirect("profile")

@login_required
def dashboard_live(request):

    reservations = Reservation.objects.select_related(
        "user",
        "barber__user",
        "service"
    )

    if request.user.is_barber:
        reservations = reservations.filter(
            barber__user=request.user
        )

    reservations = reservations.order_by("-created_at")[:8]

    data = []

    for reservation in reservations:

        if reservation.user:
            customer_name = reservation.user.full_name
        else:
            customer_name = reservation.customer_name

        jalali_date = jdatetime.date.fromgregorian(
            date=reservation.date
        ).strftime("%Y/%m/%d")

        data.append({
            "id": reservation.id,
            "customer_name": customer_name,
            "service": reservation.service.name,
            "barber": reservation.barber.user.full_name,
            "date": jalali_date,
            "time": reservation.time.strftime("%H:%M"),
            "status": reservation.get_status_display(),
        })

    return JsonResponse({
        "reservation_count": Reservation.objects.count(),
        "reservations": data,
    })

from core.models import ConsultationRequest

@login_required
def consultation_requests(request):

    requests = ConsultationRequest.objects.all().order_by("-created_at")

    return render(
        request,
        "superadmin_panel/consultation_requests.html",
        {
            "requests": requests
        }
    )
@login_required
def consultation_request_detail(request, request_id):

    consultation = get_object_or_404(
        ConsultationRequest,
        id=request_id
    )

    if not consultation.is_read:
        consultation.is_read = True
        consultation.save(update_fields=["is_read"])

    return render(
        request,
        "superadmin_panel/consultation_request_detail.html",
        {
            "consultation": consultation
        }
    )
@login_required
def users_list(request):

    users = CustomUser.objects.all().order_by("-id")

    context = {

        "users": users,

    }

    return render(
        request,
        "superadmin_panel/users.html",
        context
    )



@login_required
def user_detail(request, id):

    user = get_object_or_404(
        CustomUser,
        id=id
    )

    reservations = Reservation.objects.filter(
        user=user
    ).select_related(
        "barber__user",
        "service"
    ).order_by(
        "-date",
        "-time"
    )

    orders = Order.objects.filter(
        user=user
    ).order_by(
        "-created_at"
    )

    gallery_images = user.gallery_images.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "superadmin_panel/user_detail.html",
        {
            "user_obj": user,
            "reservations": reservations,
            "orders": orders,
            "gallery_images": gallery_images,
        }
    )


@login_required
def user_edit(request, id):

    user = CustomUser.objects.get(id=id)

    if request.method == "POST":

        form = UserEditForm(
            request.POST,
            request.FILES,
            instance=user
        )

        if form.is_valid():

            user = form.save()

            role = request.POST.get("role")

            # حذف همه گروه‌های قبلی
            user.groups.clear()

            # اگر نقش انتخاب شده کاربر عادی نبود
            if role != "user":

                group = Group.objects.get(name=role)

                user.groups.add(group)

            return redirect("superadmin_users")

    else:

        form = UserEditForm(instance=user)

    context = {

        "form": form,
        "user_obj": user,
        "groups": Group.objects.all(),

    }

    return render(
        request,
        "superadmin_panel/user_edit.html",
        context
    )
@login_required
def barbers_list(request):

    barbers = Barber.objects.select_related("user").all()

    return render(
        request,
        "superadmin_panel/barbers.html",
        {
            "barbers": barbers
        }
    )
@login_required
def barber_edit(request, id):

    barber = get_object_or_404(
        Barber,
        id=id
    )

    if request.method == "POST":

        form = BarberEditForm(
            request.POST,
            instance=barber
        )

        if form.is_valid():

            form.save()

            # -----------------------------
            # بروزرسانی روزهای کاری
            # -----------------------------

            BarberWorkingDay.objects.filter(
                barber=barber
            ).delete()

            working_days = form.cleaned_data.get(
                "working_days",
                []
            )

            for day in working_days:

                BarberWorkingDay.objects.create(
                    barber=barber,
                    day=int(day),
                    is_working=True
                )

            messages.success(
                request,
                "اطلاعات آرایشگر با موفقیت ویرایش شد."
            )

            return redirect(
                "superadmin_barbers"
            )

    else:

        existing_days = BarberWorkingDay.objects.filter(
            barber=barber,
            is_working=True
        ).values_list(
            "day",
            flat=True
        )

        form = BarberEditForm(
            instance=barber,
            initial={
                "working_days": [
                    str(day)
                    for day in existing_days
                ]
            }
        )

    return render(
        request,
        "superadmin_panel/barber_edit.html",
        {
            "form": form,
            "barber": barber,
        }
    )
@login_required
def barber_add(request, user_id):

    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":

        form = BarberForm(request.POST)

        if form.is_valid():

            barber = form.save(commit=False)

            barber.user = user

            barber.save()

            # -----------------------------
            # ذخیره روزهای کاری
            # -----------------------------

            working_days = form.cleaned_data.get(
                "working_days",
                []
            )

            for day in working_days:

                BarberWorkingDay.objects.create(
                    barber=barber,
                    day=int(day),
                    is_working=True
                )

            # -----------------------------
            # اضافه کردن کاربر به گروه Barber
            # -----------------------------

            from django.contrib.auth.models import Group

            barber_group, created = Group.objects.get_or_create(
                name="Barber"
            )

            user.groups.add(barber_group)

            return redirect("superadmin_barbers")

    else:

        form = BarberForm()

    return render(
        request,
        "superadmin_panel/barber_add_form.html",
        {
            "form": form,
            "user_obj": user,
        }
    )
@login_required
def search_users(request):

    query = request.GET.get("q", "")

    users = CustomUser.objects.filter(
        barber__isnull=True
    )

    if query:

        users = users.filter(
            full_name__icontains=query
        ) | users.filter(
            phone__icontains=query
        )

    data = []

    for user in users[:20]:

        data.append({
            "id": user.id,
            "full_name": user.full_name,
            "phone": user.phone,
        })

    return JsonResponse(data, safe=False)

@login_required
def barber_search(request):

    return render(
        request,
        "superadmin_panel/barber_add.html"
    )

@login_required
def reservations_list(request):

    reservations = Reservation.objects.select_related(
        "user",
        "barber__user",
        "service"
    )

    # ---------------------------------
    # اگر آرایشگر باشد فقط نوبت‌های خودش
    # ---------------------------------

    if request.user.is_barber:

        reservations = reservations.filter(
            barber__user=request.user
        )

    # ---------------------------------
    # فیلترهای سوپر ادمین / مدیر
    # ---------------------------------

    else:

        search = request.GET.get("search")

        barber = request.GET.get("barber")

        date = request.GET.get("date")


        if search:

            reservations = reservations.filter(
                Q(user__full_name__icontains=search) |
                Q(customer_name__icontains=search)
            )


        if barber:

            reservations = reservations.filter(
                barber_id=barber
            )


        if date:

            reservations = reservations.filter(
                date=date
            )


    # ---------------------------------
    # تشخیص حالت نمایش
    # ---------------------------------

    show_past = request.GET.get("past") == "1"
    


    # تاریخ و ساعت فعلی
    now = timezone.localtime()

    today = now.date()

    current_time = now.time()


    # ---------------------------------
    # نوبت‌های گذشته
    # ---------------------------------

    if show_past:

        reservations = reservations.filter(

            Q(date__lt=today) |

            Q(
                date=today,
                time__lt=current_time
            )

        ).order_by(
            "-date",
            "-time"
        )


    # ---------------------------------
    # نوبت‌های پیش‌رو
    # ---------------------------------

    else:

        reservations = reservations.filter(

            Q(date__gt=today) |

            Q(
                date=today,
                time__gte=current_time
            )

        ).order_by(
            "date",
            "time"
        )


    # ---------------------------------
    # تبدیل تاریخ میلادی به شمسی
    # ---------------------------------

    for reservation in reservations:

        reservation.jalali_date = (
            jdatetime.date.fromgregorian(
                date=reservation.date
            ).strftime("%Y/%m/%d")
        )


    # ---------------------------------
    # Context
    # ---------------------------------

    context = {

        "reservations": reservations,

        "barbers": Barber.objects.select_related(
            "user"
        ).all(),

        "show_past": show_past,

    }


    return render(
        request,
        "superadmin_panel/reservations.html",
        context
    )
@login_required
def reservations_live(request):

    reservations = Reservation.objects.select_related(
        "user",
        "barber__user",
        "service"
    )

    # ---------------------------------
    # اگر آرایشگر باشد فقط نوبت‌های خودش
    # ---------------------------------

    if request.user.is_barber:

        reservations = reservations.filter(
            barber__user=request.user
        )

    # ---------------------------------
    # فیلترهای ادمین
    # ---------------------------------

    else:

        search = request.GET.get("search")
        barber = request.GET.get("barber")
        date = request.GET.get("date")

        if search:

            reservations = reservations.filter(
                Q(user__full_name__icontains=search) |
                Q(customer_name__icontains=search)
            )

        if barber:

            reservations = reservations.filter(
                barber_id=barber
            )

        if date:

            reservations = reservations.filter(
                date=date
            )

    # ---------------------------------
    # پیش‌رو / گذشته
    # ---------------------------------

    show_past = request.GET.get("past") == "1"

    now = timezone.localtime()

    today = now.date()
    current_time = now.time()

    if show_past:

        reservations = reservations.filter(
            Q(date__lt=today) |
            Q(
                date=today,
                time__lt=current_time
            )
        ).order_by(
            "-date",
            "-time"
        )

    else:

        reservations = reservations.filter(
            Q(date__gt=today) |
            Q(
                date=today,
                time__gte=current_time
            )
        ).order_by(
            "date",
            "time"
        )

    # ---------------------------------
    # تبدیل به JSON
    # ---------------------------------

    data = []

    for reservation in reservations:

        if reservation.user:
            customer_name = reservation.user.full_name
        else:
            customer_name = reservation.customer_name

        jalali_date = jdatetime.date.fromgregorian(
            date=reservation.date
        ).strftime("%Y/%m/%d")

        data.append({

            "id": reservation.id,

            "customer_name": customer_name,

            "service": reservation.service.name,

            "service_price": reservation.service_price or 0,

            "paid_amount": reservation.paid_amount or 0,

            "remaining_amount": reservation.remaining_amount or 0,

            "barber": reservation.barber.user.full_name,

            "date": jalali_date,

            "time": reservation.time.strftime("%H:%M"),

            "status": reservation.status,

            "status_display": reservation.get_status_display(),

        })

    return JsonResponse({
        "reservations": data
    })
@login_required

def reservation_status(request, id):

    reservation = get_object_or_404(
        Reservation,
        id=id
    )

    if request.method == "POST":

        status = request.POST.get("status")

        old_status = reservation.status

        reservation.status = status
        reservation.save()

        # =====================================================
        # ارسال پیامک نظرسنجی بعد از انجام شدن نوبت
        # =====================================================

        if (
            status == "done"
            and old_status != "done"
            and not reservation.survey_sms_sent
        ):

            # لینک اختصاصی نظرسنجی
            link = request.build_absolute_uri(
                f"/reservation/survey/{reservation.survey_token}/"
            )

            send_survey_sms(
                reservation.customer_phone,
                reservation.customer_name,
                link
            )

            reservation.survey_sms_sent = True

            reservation.save(
                update_fields=["survey_sms_sent"]
            )

    return redirect("superadmin_reservations")


@login_required
def reservation_delete(request, id):

    reservation = Reservation.objects.get(id=id)

    reservation.delete()

    return redirect("superadmin_reservations")

@login_required
@permission_required("services_access")
def services_list(request):

    services = Service.objects.all().order_by("order")

    return render(
        request,
        "superadmin_panel/services.html",
        {
            "services": services
        }
    )
@login_required
def service_add(request):

    if request.method == "POST":

        form = ServiceForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            service = form.save()

            # ==========================================
            # قیمت و زمان اصلی هر آرایشگر
            # ==========================================

            for barber in service.barbers.all():

                price = request.POST.get(
                    f"barber_price_{barber.id}"
                )

                duration = request.POST.get(
                    f"barber_duration_{barber.id}"
                )

                if price:

                    BarberServicePrice.objects.update_or_create(
                        service=service,
                        barber=barber,
                        defaults={
                            "price": int(price),
                            "duration": int(duration or 30),
                        }
                    )

            # ==========================================
            # جزئیات خدمت
            # ==========================================

            detail_indexes = request.POST.getlist(
                "detail_indexes"
            )

            for index in detail_indexes:

                name = request.POST.get(
                    f"detail_name_{index}",
                    ""
                ).strip()

                if not name:
                    continue

                detail = ServiceDetail.objects.create(
                    service=service,

                    name=name,

                    description=request.POST.get(
                        f"detail_description_{index}",
                        ""
                    ).strip(),

                    order=int(
                        request.POST.get(
                            f"detail_order_{index}",
                            0
                        ) or 0
                    ),

                    is_active=(
                        request.POST.get(
                            f"detail_active_{index}"
                        ) == "on"
                    ),
                )

                # ======================================
                # قیمت و زمان جزئیات برای هر آرایشگر
                # ======================================

                for barber in service.barbers.all():

                    selected = request.POST.get(
                        f"detail_barber_{index}_{barber.id}"
                    )

                    if not selected:
                        continue

                    price = request.POST.get(
                        f"detail_price_{index}_{barber.id}"
                    )

                    duration = request.POST.get(
                        f"detail_duration_{index}_{barber.id}"
                    )

                    if price:

                        BarberServiceDetailPrice.objects.create(

                            detail=detail,

                            barber=barber,

                            price=int(price),

                            duration=int(
                                duration or 10
                            )
                        )

            messages.success(
                request,
                "خدمت با موفقیت اضافه شد."
            )

            return redirect(
                "superadmin_services"
            )

    else:

        form = ServiceForm()

        # ==========================================
    # اطلاعات آرایشگرها برای HTML و JavaScript
    # ==========================================

    barber_rows = []

    for barber in form.fields["barbers"].queryset:

        barber_rows.append({

            "barber": barber,

            "selected": False,

            "price": "",

            "duration": 30,

        })


    # ==========================================
    # اطلاعات JSON-safe برای JavaScript
    # ==========================================

    barber_data = []

    for barber in form.fields["barbers"].queryset:

        barber_data.append({

            "id": barber.id,

            "full_name": barber.user.full_name,

        })


    return render(
        request,
        "superadmin_panel/service_form.html",
        {
            "form": form,

            "title": "افزودن خدمت",

            "barber_rows": barber_rows,

            "barber_data": barber_data,

            "detail_rows": [],
        }
    )

@login_required
def service_gallery(request, id):

    service = get_object_or_404(
        Service,
        id=id
    )

    images = service.images.all()

    return render(
        request,
        "superadmin_panel/service_gallery.html",
        {
            "service": service,
            "images": images,
        },
    )


@login_required
def add_service_gallery(request, id):

    service = get_object_or_404(
        Service,
        id=id
    )

    if request.method == "POST":

        images = request.FILES.getlist("images")

        for image in images:

            ServiceImage.objects.create(
                service=service,
                image=image
            )

        return redirect(
            "service_gallery",
            id=service.id
        )

    return render(
        request,
        "superadmin_panel/add_service_gallery.html",
        {
            "service": service,
        }
    )


@login_required
def delete_service_gallery(request, image_id):

    image = get_object_or_404(
        ServiceImage,
        id=image_id
    )

    service_id = image.service.id

    if request.method == "POST":

        image.delete()

        return redirect(
            "service_gallery",
            id=service_id
        )

    return render(
        request,
        "superadmin_panel/delete_service_gallery.html",
        {
            "image": image,
        }
    )
@login_required
def service_edit(request, id):

    service = get_object_or_404(
        Service,
        id=id
    )

    if request.method == "POST":

        form = ServiceForm(
            request.POST,
            request.FILES,
            instance=service
        )

        if form.is_valid():

            service = form.save()

            # ==========================================
            # بروزرسانی قیمت و زمان اصلی آرایشگرها
            # ==========================================

            BarberServicePrice.objects.filter(
                service=service
            ).delete()

            for barber in service.barbers.all():

                price = request.POST.get(
                    f"barber_price_{barber.id}"
                )

                duration = request.POST.get(
                    f"barber_duration_{barber.id}"
                )

                if price:

                    BarberServicePrice.objects.create(

                        service=service,

                        barber=barber,

                        price=int(price),

                        duration=int(
                            duration or 30
                        )
                    )

            # ==========================================
            # حذف جزئیات قبلی
            # ==========================================

            ServiceDetail.objects.filter(
                service=service
            ).delete()

            # ==========================================
            # ساخت جزئیات جدید
            # ==========================================

            detail_indexes = request.POST.getlist(
                "detail_indexes"
            )

            for index in detail_indexes:

                name = request.POST.get(
                    f"detail_name_{index}",
                    ""
                ).strip()

                if not name:
                    continue

                detail = ServiceDetail.objects.create(

                    service=service,

                    name=name,

                    description=request.POST.get(
                        f"detail_description_{index}",
                        ""
                    ).strip(),

                    order=int(
                        request.POST.get(
                            f"detail_order_{index}",
                            0
                        ) or 0
                    ),

                    is_active=(
                        request.POST.get(
                            f"detail_active_{index}"
                        ) == "on"
                    ),
                )

                # ======================================
                # قیمت و زمان هر آرایشگر
                # ======================================

                for barber in service.barbers.all():

                    selected = request.POST.get(
                        f"detail_barber_{index}_{barber.id}"
                    )

                    if not selected:
                        continue

                    price = request.POST.get(
                        f"detail_price_{index}_{barber.id}"
                    )

                    duration = request.POST.get(
                        f"detail_duration_{index}_{barber.id}"
                    )

                    if price:

                        BarberServiceDetailPrice.objects.create(

                            detail=detail,

                            barber=barber,

                            price=int(price),

                            duration=int(
                                duration or 10
                            )
                        )

            messages.success(
                request,
                "خدمت با موفقیت ویرایش شد."
            )

            return redirect(
                "superadmin_services"
            )

    else:

        form = ServiceForm(
            instance=service
        )

    # ==========================================
    # آرایشگرهای اصلی
    # ==========================================

    barber_rows = []

    for barber in form.fields["barbers"].queryset:

        existing_price = (
            BarberServicePrice.objects.filter(
                service=service,
                barber=barber
            ).first()
        )

        barber_rows.append({

            "barber": barber,

            "selected": (
                barber in service.barbers.all()
            ),

            "price": (
                existing_price.price
                if existing_price
                else ""
            ),

            "duration": (
                existing_price.duration
                if existing_price
                else 30
            ),

        })

    # ==========================================
    # جزئیات قبلی برای ویرایش
    # ==========================================

    detail_rows = []

    details = service.details.all().order_by(
        "order",
        "id"
    )

    for detail in details:

        barber_rows_for_detail = []

        for barber in service.barbers.all():

            detail_price = (
                BarberServiceDetailPrice.objects.filter(
                    detail=detail,
                    barber=barber
                ).first()
            )

            barber_rows_for_detail.append({

                "barber": barber,

                "selected": (
                    detail_price is not None
                ),

                "price": (
                    detail_price.price
                    if detail_price
                    else ""
                ),

                "duration": (
                    detail_price.duration
                    if detail_price
                    else 10
                ),

            })

        detail_rows.append({

            "name": detail.name,

            "description": detail.description,

            "order": detail.order,

            "is_active": detail.is_active,

            "barbers": barber_rows_for_detail,

        })

    return render(
        request,
        "superadmin_panel/service_form.html",
        {
            "form": form,
            "title": "ویرایش خدمت",
            "barber_rows": barber_rows,
            "detail_rows": detail_rows,
        }
    )

@login_required
def service_delete(request, id):

    service = Service.objects.get(id=id)

    service.delete()

    return redirect("superadmin_services")

@login_required
def admins_list(request):

    admins = (
        CustomUser.objects.filter(
            groups__name__in=["Admin", "SuperAdmin"]
        )
        .prefetch_related("groups")
        .select_related("admin_permission")
        .distinct()
    )

    return render(
        request,
        "superadmin_panel/admins.html",
        {
            "admins": admins
        }
    )


@login_required
def admin_permission(request, user_id):

    user = CustomUser.objects.get(id=user_id)

    permission, created = AdminPermission.objects.get_or_create(
        user=user
    )

    if request.method == "POST":

        form = AdminPermissionForm(
            request.POST,
            instance=permission
        )

        if form.is_valid():

            form.save()

            return redirect("superadmin_admins")

    else:

        form = AdminPermissionForm(
            instance=permission
        )

    return render(
        request,
        "superadmin_panel/admin_permission.html",
        {
            "form": form,
            "user_obj": user,
        }
    )
@login_required
def admin_add(request):

    users = CustomUser.objects.filter(
        groups__name="Admin"
    )

    normal_users = CustomUser.objects.exclude(
        groups__name="Admin"
    ).exclude(
        groups__name="SuperAdmin"
    )

    if request.method == "POST":

        user_id = request.POST.get("user")

        user = CustomUser.objects.get(id=user_id)

        group = Group.objects.get(name="Admin")

        user.groups.add(group)

        AdminPermission.objects.get_or_create(user=user)

        return redirect("superadmin_admins")

    return render(
        request,
        "superadmin_panel/admin_add.html",
        {
            "users": normal_users
        }
    )
@login_required
def admin_search(request):

    return render(
        request,
        "superadmin_panel/admin_search.html"
    )
@login_required
def admin_add(request, user_id):

    user = CustomUser.objects.get(id=user_id)

    group = Group.objects.get(name="Admin")

    user.groups.add(group)

    AdminPermission.objects.get_or_create(user=user)

    return redirect("superadmin_admins")
@login_required
def search_admin_users(request):

    query = request.GET.get("q", "")

    users = CustomUser.objects.exclude(
        groups__name="Admin"
    ).exclude(
        groups__name="SuperAdmin"
    )

    if query:

        users = users.filter(
            full_name__icontains=query
        ) | users.filter(
            phone__icontains=query
        )

    data = []

    for user in users[:20]:

        data.append({
            "id": user.id,
            "full_name": user.full_name,
            "phone": user.phone,
        })

    return JsonResponse(data, safe=False)
@login_required
def admin_remove(request, user_id):

    user = get_object_or_404(
        CustomUser,
        id=user_id
    )

    if request.method == "POST":

        # حذف نقش Admin فقط از این کاربر
        admin_group = Group.objects.filter(
            name="Admin"
        ).first()

        if admin_group:
            user.groups.remove(admin_group)

        # حذف تمام دسترسی‌های اختصاصی مدیر
        AdminPermission.objects.filter(
            user=user
        ).delete()

        messages.success(
            request,
            "مدیر با موفقیت از مدیریت حذف شد."
        )

    return redirect(
        "superadmin_admins"
    )
@login_required
def barber_delete(request, id):

    barber = get_object_or_404(
        Barber,
        id=id
    )

    if request.method == "POST":

        user = barber.user

        # حذف رکورد آرایشگر
        barber.delete()

        # حذف نقش Barber از کاربر
        from django.contrib.auth.models import Group

        barber_group = Group.objects.filter(
            name="Barber"
        ).first()

        if barber_group:
            user.groups.remove(barber_group)

        messages.success(
            request,
            "آرایشگر با موفقیت حذف شد."
        )

    return redirect(
        "superadmin_barbers"
    )

@login_required
def barber_blocked_times(request):

    # ==========================================
    # آرایشگرها
    # ==========================================

    barbers = Barber.objects.select_related(
        "user"
    ).all()


    # ==========================================
    # تشخیص آرایشگر / ادمین
    # ==========================================

    if getattr(request.user, "barber", False):

        # اگر خود کاربر آرایشگر است
        barber = get_object_or_404(
            Barber,
            user=request.user
        )

        selected_barber_id = barber.id

    else:

        # اگر ادمین است
        selected_barber_id = request.GET.get("barber")

        if request.method == "POST":
            selected_barber_id = request.POST.get("barber")

        barber = None

        if selected_barber_id:

            barber = get_object_or_404(
                Barber,
                id=selected_barber_id
            )


    # ==========================================
    # ثبت بازه مسدود
    # ==========================================

    if request.method == "POST":

        form = BarberBlockedTimeForm(
            request.POST
        )

        if form.is_valid():

            # اگر ادمین است حتماً باید آرایشگر انتخاب شده باشد
            if not barber:

                messages.error(
                    request,
                    "لطفاً آرایشگر را انتخاب کنید."
                )

            else:

                blocked = form.save(
                    commit=False
                )

                blocked.barber = barber

                blocked.save()

                messages.success(
                    request,
                    "بازه زمانی با موفقیت بسته شد."
                )

                return redirect(
                    "barber_blocked_times"
                )

    else:

        form = BarberBlockedTimeForm()


    # ==========================================
    # بازه‌های مسدود
    # ==========================================

    if barber:

        blocked_times = BarberBlockedTime.objects.filter(
            barber=barber
        ).order_by(
            "-date",
            "-start_time"
        )

    else:

        # برای ادمین قبل از انتخاب آرایشگر
        blocked_times = BarberBlockedTime.objects.none()


    # ==========================================
    # ارسال اطلاعات به قالب
    # ==========================================

    return render(
        request,
        "superadmin_panel/blocked_times.html",
        {
            "form": form,
            "blocked_times": blocked_times,
            "barbers": barbers,
            "selected_barber": barber,
            "selected_barber_id": selected_barber_id,
        }
    )


# =====================================================
# DELETE
# =====================================================

@login_required
def delete_blocked_time(request, pk):

    item = get_object_or_404(
        BarberBlockedTime,
        id=pk
    )


    # اگر آرایشگر است فقط بازه خودش
    if getattr(request.user, "barber", False):

        if item.barber.user != request.user:

            messages.error(
                request,
                "شما اجازه حذف این بازه را ندارید."
            )

            return redirect(
                "barber_blocked_times"
            )


    item.delete()

    messages.success(
        request,
        "بازه زمانی حذف شد."
    )

    return redirect(
        "barber_blocked_times"
    )


# =====================================================
# EDIT
# =====================================================

@login_required
def edit_blocked_time(request, pk):

    blocked = get_object_or_404(
        BarberBlockedTime,
        id=pk
    )


    # ==========================================
    # اگر آرایشگر است
    # ==========================================

    if getattr(request.user, "barber", False):

        if blocked.barber.user != request.user:

            messages.error(
                request,
                "شما اجازه ویرایش این بازه را ندارید."
            )

            return redirect(
                "barber_blocked_times"
            )


    # ==========================================
    # فرم
    # ==========================================

    if request.method == "POST":

        form = BarberBlockedTimeForm(
            request.POST,
            instance=blocked
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "بازه زمانی ویرایش شد."
            )

            return redirect(
                "barber_blocked_times"
            )

    else:

        form = BarberBlockedTimeForm(
            instance=blocked
        )


    # ==========================================
    # لیست آرایشگرها
    # ==========================================

    barbers = Barber.objects.select_related(
        "user"
    ).all()


    blocked_times = BarberBlockedTime.objects.filter(
        barber=blocked.barber
    ).order_by(
        "-date",
        "-start_time"
    )


    return render(
        request,
        "superadmin_panel/blocked_times.html",
        {
            "form": form,
            "blocked_times": blocked_times,
            "barbers": barbers,
            "selected_barber": blocked.barber,
            "selected_barber_id": blocked.barber.id,
            "editing": True,
            "editing_blocked": blocked,
        }
    )
@login_required
def barber_walkin_reservation(request):

    is_admin = (
        request.user.is_superuser
        or request.user.admin_permission
    )

    # =========================
    # آرایشگرهای موجود
    # =========================

    barbers = Barber.objects.select_related("user").all()

    # =========================
    # تعیین آرایشگر
    # =========================

    if is_admin:

        barber_id = request.POST.get("barber") or request.GET.get("barber")

        if barber_id:

            try:
                barber = Barber.objects.get(id=barber_id)
            except Barber.DoesNotExist:
                messages.error(
                    request,
                    "آرایشگر انتخاب شده پیدا نشد."
                )
                barber = None

        else:

            barber = None

    else:

        try:
            barber = Barber.objects.get(
                user=request.user
            )
        except Barber.DoesNotExist:

            messages.error(
                request,
                "حساب شما به عنوان آرایشگر ثبت نشده است."
            )

            return redirect("superadmin")

    # =========================
    # POST
    # =========================

    if request.method == "POST":

        form = WalkInReservationForm(request.POST)

        if not barber:

            messages.error(
                request,
                "لطفاً یک آرایشگر انتخاب کنید."
            )

        elif form.is_valid():

            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]

            service = form.cleaned_data["service"]

            # =========================
            # بررسی نوبت موجود
            # =========================

            reservation_exists = Reservation.objects.filter(
                barber=barber,
                date=date,
                time=time
            ).exists()

            # =========================
            # بررسی ساعت مسدود
            # =========================

            blocked_exists = BarberBlockedTime.objects.filter(
                barber=barber,
                date=date,
                start_time__lte=time,
                end_time__gt=time
            ).exists()

            if reservation_exists or blocked_exists:

                messages.error(
                    request,
                    "این ساعت برای این آرایشگر در دسترس نیست."
                )

            else:

                # =========================
                # پیدا کردن قیمت خدمت
                # =========================

                barber_service_price = BarberServicePrice.objects.filter(
                    barber=barber,
                    service=service
                ).first()

                if not barber_service_price:

                    messages.error(
                        request,
                        "قیمت این خدمت برای آرایشگر انتخاب‌شده ثبت نشده است."
                    )

                else:

                    service_price = barber_service_price.price

                    # =========================
                    # ثبت نوبت حضوری
                    # =========================

                    Reservation.objects.create(

                        user=None,

                        customer_name=form.cleaned_data[
                            "customer_name"
                        ],

                        customer_phone=form.cleaned_data[
                            "customer_phone"
                        ],

                        barber=barber,

                        service=service,

                        date=date,

                        time=time,

                        service_price=service_price,

                        deposit_amount=0,

                        paid_amount=service_price,

                        payment_status="paid",

                        status="approved"

                    )

                    messages.success(
                        request,
                        "نوبت حضوری با موفقیت ثبت شد."
                    )

                    if is_admin:

                        return redirect(
                            "barber_walkin_reservation"
                        )

                    return redirect(
                        "barber_walkin_reservation"
                    )

    else:

        form = WalkInReservationForm()

    # =========================
    # لیست نوبت‌ها
    # =========================

    if is_admin:

        reservations = Reservation.objects.all().order_by(
            "-date",
            "-time"
        )

    else:

        reservations = Reservation.objects.filter(
            barber=barber
        ).order_by(
            "-date",
            "-time"
        )

    return render(
        request,
        "superadmin_panel/barber_walkin.html",
        {
            "form": form,
            "reservations": reservations,
            "barbers": barbers,
            "selected_barber": barber,
            "is_admin": is_admin,
        }
    )
@login_required
def barber_walkin_busy_times(request):

    is_admin = (
        request.user.is_superuser
        or request.user.admin_permission
    )

    # =========================
    # تعیین آرایشگر
    # =========================

    if is_admin:

        barber_id = request.GET.get("barber_id")

        if not barber_id:

            return JsonResponse([], safe=False)

        try:

            barber = Barber.objects.get(
                id=barber_id
            )

        except Barber.DoesNotExist:

            return JsonResponse([], safe=False)

    else:

        try:

            barber = Barber.objects.get(
                user=request.user
            )

        except Barber.DoesNotExist:

            return JsonResponse([], safe=False)

    # =========================
    # تاریخ
    # =========================

    date = request.GET.get("date")

    if not date:

        return JsonResponse([], safe=False)

    # =========================
    # رزروها
    # =========================

    reservations = Reservation.objects.filter(
        barber=barber,
        date=date
    )

    # =========================
    # ساعات مسدود
    # =========================

    blocked_times = BarberBlockedTime.objects.filter(
        barber=barber,
        date=date
    )

    data = []

    # =========================
    # نوبت‌های رزرو شده
    # =========================

    for reservation in reservations:

        data.append(
            reservation.time.strftime("%H:%M")
        )

    # =========================
    # زمان‌های مسدود شده
    # =========================

    for blocked in blocked_times:

        current = blocked.start_time

        while current < blocked.end_time:

            data.append(
                current.strftime("%H:%M")
            )

            total_minutes = (
                current.hour * 60
                + current.minute
                + barber.appointment_duration
            )

            hour = total_minutes // 60
            minute = total_minutes % 60

            if hour >= 24:
                break

            current = current.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

    return JsonResponse(
        list(set(data)),
        safe=False
    )

@login_required
def academy_courses(request):

    courses = Course.objects.all().order_by("-id")

    return render(
        request,
        "superadmin_panel/courses.html",
        {
            "courses": courses,
        },
    )


@login_required
def academy_course_add(request):

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "دوره با موفقیت اضافه شد."
            )

            return redirect("academy_courses")

    else:

        form = CourseForm()

    return render(
        request,
        "superadmin_panel/course_form.html",
        {
            "form": form,
            "title": "افزودن دوره",
        },
    )


@login_required
def academy_course_edit(request, pk):

    course = get_object_or_404(
        Course,
        id=pk
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "دوره ویرایش شد."
            )

            return redirect("academy_courses")

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "superadmin_panel/course_form.html",
        {
            "form": form,
            "title": "ویرایش دوره",
        },
    )


@login_required
def academy_course_delete(request, pk):

    course = get_object_or_404(
        Course,
        id=pk
    )

    course.delete()

    messages.success(
        request,
        "دوره حذف شد."
    )

    return redirect("academy_courses")
@staff_member_required
def course_students(request, pk):

    course = get_object_or_404(Course, pk=pk)

    students = (
        CourseStudent.objects
        .filter(course=course)
        .select_related("user")
    )

    return render(
        request,
        "superadmin_panel/course_students.html",
        {
            "course": course,
            "students": students,
        },
    )


@staff_member_required
def all_course_students(request):

    students = (
        CourseStudent.objects
        .select_related("course", "user")
        .order_by("-created_at")
    )

    return render(
        request,
        "superadmin_panel/all_course_students.html",
        {
            "students": students,
        },
    )

@staff_member_required
def course_topics(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    topics = course.topics.all().order_by("order")

    return render(
        request,
        "superadmin_panel/course_topics.html",
        {
            "course": course,
            "topics": topics,
        }
    )
@login_required
def course_sessions(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    sessions = course.sessions.all().order_by("order")

    return render(
        request,
        "superadmin_panel/course_sessions.html",
        {
            "course": course,
            "sessions": sessions,
        }
    )
@login_required
def add_course_session(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        title = request.POST.get("title")
        order = request.POST.get("order")

        CourseSession.objects.create(
            course=course,
            title=title,
            order=order,
        )

        return redirect(
            "academy_course_sessions",
            pk=course.id
        )

    return render(
        request,
        "superadmin_panel/add_course_session.html",
        {
            "course": course,
        }
    )
@login_required
def edit_course_session(request, session_id):

    session = get_object_or_404(
        CourseSession,
        id=session_id
    )

    if request.method == "POST":

        session.title = request.POST.get("title")

        session.order = request.POST.get("order")

        session.save()

        return redirect(
            "academy_course_sessions",
            pk=session.course.id
        )

    return render(
        request,
        "superadmin_panel/edit_course_session.html",
        {
            "session": session,
        }
    )
@login_required
def delete_course_session(request, session_id):

    session = get_object_or_404(
        CourseSession,
        id=session_id
    )

    course_id = session.course.id

    if request.method == "POST":

        session.delete()

        return redirect(
            "academy_course_sessions",
            pk=course_id
        )

    return render(
        request,
        "superadmin_panel/delete_course_session.html",
        {
            "session": session,
        }
    )
@login_required
def course_features(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    features = course.features.all()

    return render(
        request,
        "superadmin_panel/course_features.html",
        {
            "course": course,
            "features": features,
        }
    )
@login_required
def add_course_feature(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        CourseFeature.objects.create(
            course=course,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            icon=request.POST.get("icon"),
        )

        return redirect(
            "academy_course_features",
            pk=course.id
        )

    return render(
        request,
        "superadmin_panel/add_course_feature.html",
        {
            "course": course,
        }
    )

@login_required
def course_manage(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    return render(
        request,
        "superadmin_panel/course_manage.html",
        {
            "course": course,
        }
    )
@login_required
def edit_course_feature(request, feature_id):

    feature = get_object_or_404(
        CourseFeature,
        id=feature_id
    )

    if request.method == "POST":

        feature.title = request.POST.get("title")
        feature.description = request.POST.get("description")
        feature.icon = request.POST.get("icon")

        feature.save()

        return redirect(
            "academy_course_features",
            pk=feature.course.id
        )

    return render(
        request,
        "superadmin_panel/edit_course_feature.html",
        {
            "feature": feature,
        }
    )
@login_required
def delete_course_feature(request, feature_id):

    feature = get_object_or_404(
        CourseFeature,
        id=feature_id
    )

    course_id = feature.course.id

    if request.method == "POST":

        feature.delete()

        return redirect(
            "academy_course_features",
            pk=course_id
        )

    return render(
        request,
        "superadmin_panel/delete_course_feature.html",
        {
            "feature": feature,
        }
    )
@login_required
def course_gallery(request, pk):

    course = get_object_or_404(Course, pk=pk)

    images = course.gallery.all()

    return render(
        request,
        "superadmin_panel/course_gallery.html",
        {
            "course": course,
            "images": images,
        },
    )
@login_required
def add_course_gallery(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        if request.FILES.get("image"):

            CourseImage.objects.create(
                course=course,
                image=request.FILES["image"]
            )

            return redirect(
                "academy_course_gallery",
                pk=course.id
            )

    return render(
        request,
        "superadmin_panel/add_course_gallery.html",
        {
            "course": course,
        }
    )
@login_required
def delete_course_gallery(request, image_id):

    image = get_object_or_404(
        CourseImage,
        id=image_id
    )

    course_id = image.course.id

    if request.method == "POST":

        image.delete()

        return redirect(
            "academy_course_gallery",
            pk=course_id
        )

    return render(
        request,
        "superadmin_panel/delete_course_gallery.html",
        {
            "image": image,
        }
    )
from shop.models import Product
from shop.models import Product

def products(request):

    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(
        request,
        "superadmin_panel/products.html",
        context,
    )

from shop.forms import ProductForm
from django.shortcuts import redirect

def add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()
           
            return redirect("products")

    else:

        form = ProductForm()

    context = {

        "form": form,

    }

    return render(
        request,
        "superadmin_panel/product_form.html",
        context,
    )
from django.shortcuts import get_object_or_404

def edit_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    print(product.related_products.all())

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid():

            form.save()

            return redirect("products")

    else:

        form = ProductForm(instance=product)

    return render(
        request,
        "superadmin_panel/product_form.html",
        {
            "form": form,
            "product": product,
        },
    )
from shop.models import Product, ProductImage
def product_gallery(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    if request.method == "POST":

        images = request.FILES.getlist("images")


        if images:

            for image in images:

                ProductImage.objects.create(
                    product=product,
                    image=image
                )


            messages.success(
                request,
                "تصاویر با موفقیت اضافه شدند."
            )


            return redirect(
                "product_gallery",
                product_id=product.id
            )


    images = product.gallery.all()


    return render(
        request,
        "superadmin_panel/product_gallery.html",
        {
            "product": product,
            "images": images,
        },
    )

def delete_product_image(request, image_id):

    image = get_object_or_404(
        ProductImage,
        id=image_id
    )

    product_id = image.product.id

    if request.method == "POST":

        image.delete()

        messages.success(
            request,
            "تصویر حذف شد."
        )


    return redirect(
        "product_gallery",
        product_id=product_id
    )
from shop.models import Category
def categories(request):

    categories = Category.objects.all()

    return render(
        request,
        "superadmin_panel/categories.html",
        {
            "categories": categories,
        },
    )

from shop.forms import CategoryForm

def add_category(request):

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("categories")

    else:

        form = CategoryForm()

    return render(
        request,
        "superadmin_panel/category_form.html",
        {
            "form": form,
        },
    )
def shop_management(request):
    return render(
        request,
        "superadmin_panel/shop_management.html"
    )
from shop.models import Brand
from shop.forms import BrandForm
from django.shortcuts import render, redirect
from shop.forms import BrandForm

def brands(request):

    brands = Brand.objects.all()

    return render(
        request,
        "superadmin_panel/brands.html",
        {
            "brands": brands
        }
    )


def add_brand(request):

    if request.method == "POST":

        form = BrandForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return redirect("brands")

    else:

        form = BrandForm()


    return render(
        request,
        "superadmin_panel/brand_form.html",
        {
            "form": form
        }
    )

def delete_brand(request, brand_id):

    brand = get_object_or_404(
        Brand,
        id=brand_id
    )

    brand.delete()

    return redirect("brands")

def edit_brand(request, brand_id):

    brand = get_object_or_404(
        Brand,
        id=brand_id
    )

    if request.method == "POST":

        form = BrandForm(
            request.POST,
            request.FILES,
            instance=brand
        )

        if form.is_valid():

            form.save()

            return redirect("brands")

    else:

        form = BrandForm(instance=brand)


    return render(
        request,
        "superadmin_panel/brand_form.html",
        {
            "form": form,
            "edit": True
        }
    )

from shop.models import ProductImage, ProductSpecification, ProductFeature
from shop.forms import ProductImageForm, ProductSpecificationForm, ProductFeatureForm


def product_specifications(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    specs = product.specifications.all()

    form = ProductSpecificationForm()

    if request.method == "POST":

        form = ProductSpecificationForm(request.POST)

        if form.is_valid():

            spec = form.save(commit=False)

            spec.product = product

            spec.save()

            return redirect("product_specifications", product.id)

    return render(
        request,
        "superadmin_panel/product_specifications.html",
        {
            "product": product,
            "specs": specs,
            "form": form,
        }
    )
def product_features(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    features = product.features.all()

    form = ProductFeatureForm()

    if request.method == "POST":

        form = ProductFeatureForm(request.POST)

        if form.is_valid():

            feature = form.save(commit=False)

            feature.product = product

            feature.save()

            return redirect("product_features", product.id)

    return render(
        request,
        "superadmin_panel/product_features.html",
        {
            "product": product,
            "features": features,
            "form": form,
        }
    )

from shop.models import Order
def orders(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    orders = Order.objects.all()

    if search:

        orders = orders.filter(
            tracking_code__iexact=search
        )

    orders = orders.order_by("-created_at")

    return render(
        request,
        "superadmin_panel/orders.html",
        {
            "orders": orders,
            "search": search,
        }
    )

from django.shortcuts import get_object_or_404, redirect

def delete_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.delete()
        return redirect("orders")

    return redirect("orders")
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    return render(
        request,
        "superadmin_panel/order_detail.html",
        {
            "order": order,
        }
    )
def update_order_status(request, id):

    if request.method == "POST":

        order = get_object_or_404(
            Order,
            id=id
        )

        status = request.POST.get("status")

        # وضعیت قبلی سفارش
        old_status = order.status

        order.status = status
        order.save()

        # ==========================================
        # ارسال SMS تایید سفارش
        # فقط هنگام تغییر به paid
        # و فقط یک بار
        # ==========================================

        if (
            status == "paid"
            and old_status != "paid"
            and not order.confirmation_sms_sent
        ):

            response = send_order_confirmation_sms(
                phone=order.phone,
                name=order.full_name,
                order_number=order.tracking_code,
                price=order.total_price,
            )

            if response and response.status_code in [200, 201]:

                order.confirmation_sms_sent = True

                order.save(
                    update_fields=[
                        "confirmation_sms_sent"
                    ]
                )

    return redirect(
        "order_detail",
        id=id
    )

@login_required(login_url="/login/")
def superadmin_settings(request):

    return render(
        request,
        "superadmin_panel/settings.html"
    )

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

@login_required
def superadmin_change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
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

            return redirect("superadmin_settings")

    else:

        form = PasswordChangeForm(request.user)

    return render(
        request,
       "superadmin_panel/change_password.html",
        {
            "form": form
        }
    )

from core.models import ContactMessage
def contact_messages(request):

    messages = ContactMessage.objects.order_by("-created_at")

    return render(
        request,
        "superadmin_panel/messages.html",
        {
            "messages": messages
        }
    )

def contact_message_detail(request, id):

    message = get_object_or_404(
        ContactMessage,
        id=id
    )

    message.is_read = True
    message.save()

    return render(
        request,
        "superadmin_panel/message_detail.html",
        {
            "message": message
        }
    )

def contact_message_delete(request, id):

    message = get_object_or_404(
        ContactMessage,
        id=id
    )

    message.delete()

    return redirect("contact_messages")

from shop.models import ProductComment

def comments(request):

    comments = ProductComment.objects.all().order_by("-created_at")


    return render(
        request,
        "superadmin_panel/comments.html",
        {
            "comments": comments
        }
    )

from django.shortcuts import get_object_or_404, redirect


def activate_comment(request, id):

    comment = get_object_or_404(
        ProductComment,
        id=id
    )

    comment.is_active = True
    comment.save()

    return redirect("superadmin_comments")



def deactivate_comment(request, id):

    comment = get_object_or_404(
        ProductComment,
        id=id
    )

    comment.is_active = False
    comment.save()

    return redirect("superadmin_comments")



def delete_comment(request, id):

    comment = get_object_or_404(
        ProductComment,
        id=id
    )

    comment.delete()

    return redirect("superadmin_comments")


from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json

from shop.models import Order

from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from datetime import timedelta
from core.models import ActivityLog

from reservation.models import Reservation
from shop.models import Order
@login_required
def reports(request):

    now = timezone.now()

    # نمودار درآمد
    income_data = (
        Order.objects.filter(status="paid")
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_price"))
        .order_by("month")
    )

    months = []
    totals = []

    for item in income_data:
        months.append(item["month"].strftime("%Y/%m"))
        totals.append(item["total"] or 0)


    # درآمد امروز
    today_income = (
        Order.objects.filter(
            status="paid",
            created_at__date=now.date()
        )
        .aggregate(
            total=Sum("total_price")
        )["total"] or 0
    )


    # درآمد این ماه
    month_income = (
        Order.objects.filter(
            status="paid",
            created_at__year=now.year,
            created_at__month=now.month
        )
        .aggregate(
            total=Sum("total_price")
        )["total"] or 0
    )


    # رزروهای امروز
    today_reservations = Reservation.objects.filter(
        date=now.date()
    ).count()


    # کل سفارشات
    total_orders = Order.objects.count()


    # کاربران جدید ۳۰ روز اخیر
    new_users = CustomUser.objects.filter(
        created_at__gte=now - timedelta(days=30)
    ).count()


    # پیام‌های خوانده نشده
    new_messages = ContactMessage.objects.filter(
        is_read=False
    ).count()
    activities = ActivityLog.objects.select_related(
    "user"
).order_by(
    "-created_at"
)[:10]


    context = {

        "months": json.dumps(months),

        "totals": json.dumps(totals),

        "today_income": today_income,

        "month_income": month_income,

        "today_reservations": today_reservations,

        "total_orders": total_orders,

        "new_users": new_users,

        "new_messages": new_messages,

        "activities": activities,

    }


    return render(
        request,
        "superadmin_panel/reports.html",
        context
    )
from core.models import ContactMessage

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model

def superadmin_user_delete(request, id):

    User = get_user_model()

    user = get_object_or_404(
        User,
        id=id
    )

    if request.method == "POST":

        user.delete()

    return redirect(
        "superadmin_users"
    )

@login_required
def customer_gallery_add(request, user_id):

    user = get_object_or_404(
        CustomUser,
        id=user_id
    )

    if request.method == "POST":

        image = request.FILES.get("image")

        if image:

            CustomerGalleryImage.objects.create(
                user=user,
                image=image
            )

            messages.success(
                request,
                "تصویر با موفقیت به گالری مشتری اضافه شد."
            )

            return redirect(
                "superadmin_user_detail",
                id=user.id
            )

    return render(
        request,
        "superadmin_panel/customer_gallery_add.html",
        {
            "user_obj": user
        }
    )


@login_required
def customer_gallery_delete(request, image_id):

    image = get_object_or_404(
        CustomerGalleryImage,
        id=image_id
    )

    user_id = image.user.id

    if request.method == "POST":

        image.delete()

        messages.success(
            request,
            "تصویر با موفقیت حذف شد."
        )

    return redirect(
        "superadmin_user_detail",
        id=user_id
    )
@login_required
def home_offers(request):

    offers = HomeOffer.objects.all().order_by("-created_at")

    return render(
        request,
        "superadmin_panel/home_offers.html",
        {
            "offers": offers,
        }
    )

@login_required
def home_offer_add(request):

    products = Product.objects.all().order_by("name")
    courses = Course.objects.all().order_by("title")

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        discount_percent = request.POST.get("discount_percent", "").strip()
        end_time = request.POST.get("end_time")
        is_active = request.POST.get("is_active") == "on"

        # ==========================================
        # اعتبارسنجی عنوان
        # ==========================================

        if not title:

            messages.error(
                request,
                "عنوان پیشنهاد را وارد کنید."
            )

            return render(
                request,
                "superadmin_panel/home_offer_form.html",
                {
                    "products": products,
                    "courses": courses,
                    "title": "افزودن پیشنهاد",
                }
            )

        # ==========================================
        # اعتبارسنجی تخفیف
        # تخفیف اختیاری است
        # ==========================================

        if discount_percent:

            try:

                discount_percent = int(
                    discount_percent
                )

            except (TypeError, ValueError):

                messages.error(
                    request,
                    "درصد تخفیف نامعتبر است."
                )

                return render(
                    request,
                    "superadmin_panel/home_offer_form.html",
                    {
                        "products": products,
                        "courses": courses,
                        "title": "افزودن پیشنهاد",
                    }
                )

            if not 0 <= discount_percent <= 100:

                messages.error(
                    request,
                    "درصد تخفیف باید بین ۰ تا ۱۰۰ باشد."
                )

                return render(
                    request,
                    "superadmin_panel/home_offer_form.html",
                    {
                        "products": products,
                        "courses": courses,
                        "title": "افزودن پیشنهاد",
                    }
                )

        else:

            discount_percent = None

        # ==========================================
        # ایجاد پیشنهاد
        # ==========================================

        offer = HomeOffer.objects.create(

            title=title,

            description=description,

            discount_percent=discount_percent,

            end_time=end_time,

            is_active=is_active,

        )

        # ==========================================
        # محصولات
        # ==========================================

        product_ids = request.POST.getlist(
            "products"
        )

        offer.products.set(
            product_ids
        )

        # ==========================================
        # دوره‌ها
        # ==========================================

        course_ids = request.POST.getlist(
            "courses"
        )

        offer.courses.set(
            course_ids
        )

        messages.success(
            request,
            "پیشنهاد با موفقیت ایجاد شد."
        )

        return redirect(
            "home_offers"
        )

    return render(
        request,
        "superadmin_panel/home_offer_form.html",
        {
            "products": products,
            "courses": courses,
            "title": "افزودن پیشنهاد",
        }
    )


@login_required
def home_offer_edit(request, pk):

    offer = get_object_or_404(
        HomeOffer,
        id=pk
    )

    products = Product.objects.all().order_by("name")
    courses = Course.objects.all().order_by("title")

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        discount_percent = request.POST.get(
            "discount_percent",
            ""
        ).strip()

        end_time = request.POST.get(
            "end_time"
        )

        is_active = (
            request.POST.get("is_active")
            == "on"
        )

        # ==========================================
        # اعتبارسنجی عنوان
        # ==========================================

        if not title:

            messages.error(
                request,
                "عنوان پیشنهاد را وارد کنید."
            )

            return render(
                request,
                "superadmin_panel/home_offer_form.html",
                {
                    "offer": offer,
                    "products": products,
                    "courses": courses,
                    "title": "ویرایش پیشنهاد",
                }
            )

        # ==========================================
        # اعتبارسنجی تخفیف
        # تخفیف اختیاری است
        # ==========================================

        if discount_percent:

            try:

                discount_percent = int(
                    discount_percent
                )

            except (TypeError, ValueError):

                messages.error(
                    request,
                    "درصد تخفیف نامعتبر است."
                )

                return render(
                    request,
                    "superadmin_panel/home_offer_form.html",
                    {
                        "offer": offer,
                        "products": products,
                        "courses": courses,
                        "title": "ویرایش پیشنهاد",
                    }
                )

            if not 0 <= discount_percent <= 100:

                messages.error(
                    request,
                    "درصد تخفیف باید بین ۰ تا ۱۰۰ باشد."
                )

                return render(
                    request,
                    "superadmin_panel/home_offer_form.html",
                    {
                        "offer": offer,
                        "products": products,
                        "courses": courses,
                        "title": "ویرایش پیشنهاد",
                    }
                )

        else:

            discount_percent = None

        # ==========================================
        # بروزرسانی پیشنهاد
        # ==========================================

        offer.title = title

        offer.description = description

        offer.discount_percent = (
            discount_percent
        )

        offer.end_time = end_time

        offer.is_active = is_active

        offer.save()

        # ==========================================
        # محصولات
        # ==========================================

        product_ids = request.POST.getlist(
            "products"
        )

        offer.products.set(
            product_ids
        )

        # ==========================================
        # دوره‌ها
        # ==========================================

        course_ids = request.POST.getlist(
            "courses"
        )

        offer.courses.set(
            course_ids
        )

        messages.success(
            request,
            "پیشنهاد با موفقیت ویرایش شد."
        )

        return redirect(
            "home_offers"
        )

    return render(
        request,
        "superadmin_panel/home_offer_form.html",
        {
            "offer": offer,
            "products": products,
            "courses": courses,
            "title": "ویرایش پیشنهاد",
        }
    )


@login_required
def home_offer_delete(request, pk):

    offer = get_object_or_404(
        HomeOffer,
        id=pk
    )

    if request.method == "POST":

        offer.delete()

        messages.success(
            request,
            "پیشنهاد حذف شد."
        )

    return redirect(
        "home_offers"
    )

@login_required
def reservation_detail(request, reservation_id):

    reservation = get_object_or_404(
        Reservation.objects.select_related(
            "user",
            "service",
            "barber__user",
        ),
        id=reservation_id
    )

    # تبدیل تاریخ میلادی به جلالی
    import jdatetime

    jalali_date = jdatetime.date.fromgregorian(
        date=reservation.date
    )

    jalali_date = (
        f"{jalali_date.year}/"
        f"{jalali_date.month:02d}/"
        f"{jalali_date.day:02d}"
    )

    return render(
        request,
        "superadmin_panel/reservation_detail.html",
        {
            "reservation": reservation,
            "jalali_date": jalali_date,
        }
    )
@login_required
def sms_management(request):

    from users.models import CustomUser
    from users.sms import send_simple_sms

    users_count = (
        CustomUser.objects
        .filter(is_active=True)
        .exclude(phone__isnull=True)
        .exclude(phone="")
        .count()
    )

    reservation_users_count = (
        Reservation.objects
        .filter(
            user__isnull=False,
            user__is_active=True
        )
        .exclude(user__phone__isnull=True)
        .exclude(user__phone="")
        .values("user")
        .distinct()
        .count()
    )

    # =========================================
    # ارسال پیامک
    # =========================================

    if request.method == "POST":

        message = request.POST.get(
            "message",
            ""
        ).strip()

        recipient_type = request.POST.get(
            "recipient_type",
            ""
        )

        # =====================================
        # بررسی متن
        # =====================================

        if not message:

            return redirect(
                "/superadmin/sms/?sms_error=متن پیامک را وارد کنید."
            )

        # =====================================
        # همه کاربران
        # =====================================

        if recipient_type == "all":

            users = (
                CustomUser.objects
                .filter(is_active=True)
                .exclude(phone__isnull=True)
                .exclude(phone="")
            )

        # =====================================
        # مشتریان دارای نوبت
        # =====================================

        elif recipient_type == "reservation":

            user_ids = (
                Reservation.objects
                .filter(
                    user__isnull=False,
                    user__is_active=True
                )
                .exclude(user__phone__isnull=True)
                .exclude(user__phone="")
                .values_list(
                    "user_id",
                    flat=True
                )
                .distinct()
            )

            users = (
                CustomUser.objects
                .filter(
                    id__in=user_ids,
                    is_active=True
                )
                .exclude(phone__isnull=True)
                .exclude(phone="")
            )

        # =====================================
        # انتخاب دستی
        # =====================================

        elif recipient_type == "manual":

            user_ids = request.POST.getlist(
                "manual_users"
            )

            users = (
                CustomUser.objects
                .filter(
                    id__in=user_ids,
                    is_active=True
                )
                .exclude(phone__isnull=True)
                .exclude(phone="")
            )

        # =====================================
        # نوع نامعتبر
        # =====================================

        else:

            return redirect(
                "/superadmin/sms/?sms_error=نوع گیرندگان نامعتبر است."
            )

        # =====================================
        # گرفتن شماره‌ها
        # =====================================

        recipients = list(
            users.values_list(
                "phone",
                flat=True
            )
        )

        # =====================================
        # بررسی گیرنده
        # =====================================

        if not recipients:

            return redirect(
                "/superadmin/sms/?sms_error=هیچ گیرنده‌ای برای ارسال پیدا نشد."
            )

        # =====================================
        # ارسال پیامک
        # =====================================

        try:

            success_count = 0

            for phone in recipients:

                response = send_simple_sms(
                    phone,
                    message
                )

                if (
                    response
                    and response.status_code == 201
                ):
                    success_count += 1

            # =================================
            # نتیجه
            # =================================

            if success_count == len(recipients):

                return redirect(
                    f"/superadmin/sms/?sms_success="
                    f"پیامک با موفقیت برای {success_count} نفر ارسال شد."
                )

            elif success_count > 0:

                return redirect(
                    f"/superadmin/sms/?sms_warning="
                    f"پیامک برای {success_count} نفر از "
                    f"{len(recipients)} نفر ارسال شد."
                )

            else:

                return redirect(
                    "/superadmin/sms/?sms_error="
                    "ارسال پیامک برای هیچ‌کدام از گیرندگان موفق نبود."
                )

        except Exception as e:

            print(
                "SMS MANAGEMENT ERROR:",
                repr(e)
            )

            return redirect(
                "/superadmin/sms/?sms_error="
                "هنگام ارسال پیامک خطایی رخ داد."
            )

    # =========================================
    # نتیجه ارسال
    # =========================================

    sms_success = request.GET.get(
        "sms_success"
    )

    sms_warning = request.GET.get(
        "sms_warning"
    )

    sms_error = request.GET.get(
        "sms_error"
    )

    # =========================================
    # نمایش صفحه
    # =========================================

    return render(
        request,
        "superadmin_panel/sms_management.html",
        {
            "users_count": users_count,
            "reservation_users_count": reservation_users_count,

            "sms_success": sms_success,
            "sms_warning": sms_warning,
            "sms_error": sms_error,
        }
    )

@login_required
def sms_search_users(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    users = CustomUser.objects.filter(
        is_active=True
    )

    if search:

        users = users.filter(
            Q(full_name__icontains=search) |
            Q(phone__icontains=search)
        )

    users = users.order_by(
        "full_name"
    )[:50]

    data = []

    for user in users:

        data.append({
            "id": user.id,
            "name": user.full_name,
            "phone": user.phone,
        })

    return JsonResponse({
        "users": data
    })



from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from discounts.models import DiscountCode
from discounts.forms import DiscountCodeForm


# =========================================================
# لیست کدهای تخفیف
# =========================================================

def superadmin_discounts(request):

    discount_codes = (
        DiscountCode.objects
        .all()
        .order_by("-created_at")
    )

    context = {
        "discount_codes": discount_codes,
    }

    return render(
        request,
        "superadmin_panel/discounts.html",
        context,
    )


# =========================================================
# ایجاد کد تخفیف
# =========================================================

def add_discount(request):

    if request.method == "POST":

        form = DiscountCodeForm(request.POST)

        if form.is_valid():

            discount = form.save()

            return redirect(
                "superadmin_discounts"
            )

    else:

        form = DiscountCodeForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "superadmin_panel/discount_form.html",
        context,
    )


# =========================================================
# ویرایش کد تخفیف
# =========================================================

def edit_discount(request, discount_id):

    discount = get_object_or_404(
        DiscountCode,
        id=discount_id
    )

    if request.method == "POST":

        form = DiscountCodeForm(
            request.POST,
            instance=discount
        )

        if form.is_valid():

            discount = form.save()

            return redirect(
                "superadmin_discounts"
            )

    else:

        form = DiscountCodeForm(
            instance=discount
        )

    context = {
        "form": form,
        "discount": discount,
    }

    return render(
        request,
        "superadmin_panel/discount_form.html",
        context,
    )
