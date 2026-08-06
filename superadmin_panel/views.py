from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from users.models import CustomUser
from reservation.models import Reservation, Barber
from services.models import Service

from .forms import UserEditForm, BarberForm
from reservation.models import Barber
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from services.models import Service
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
from academy.models import CourseStudent
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from academy.models import Course, CourseStudent
from academy.models import Course, CourseStudent,CourseSession,CourseFeature
from django.shortcuts import get_object_or_404, render
from academy.models import CourseTopic
from academy.models import CourseImage
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

    user = CustomUser.objects.get(id=id)

    context = {

        "user_obj": user,

    }

    return render(
        request,
        "superadmin_panel/user_detail.html",
        context
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
def barber_add(request, user_id):

    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":

        form = BarberForm(request.POST)

        if form.is_valid():

            barber = form.save(commit=False)

            barber.user = user

            barber.save()

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

    # اگر آرایشگر باشد فقط نوبت‌های خودش را ببیند
    if request.user.is_barber:

        reservations = reservations.filter(
            barber__user=request.user
        )

    # اگر سوپرادمین یا مدیر باشد همه نوبت‌ها را ببیند
    else:

        reservations = reservations.order_by("-date", "-time")

        search = request.GET.get("search")

        barber = request.GET.get("barber")

        date = request.GET.get("date")

        if search:

            reservations = reservations.filter(
                user__full_name__icontains=search
            )

        if barber:

            reservations = reservations.filter(
                barber_id=barber
            )

        if date:

            reservations = reservations.filter(
                date=date
            )

    context = {

        "reservations": reservations.order_by("-date", "-time"),

        "barbers": Barber.objects.select_related("user").all(),

    }

    return render(
        request,
        "superadmin_panel/reservations.html",
        context
    )



@login_required
def reservation_status(request, id):

    reservation = get_object_or_404(
        Reservation,
        id=id
    )

    if request.method == "POST":

        status = request.POST.get("status")

        reservation.status = status

        reservation.save()

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

            form.save()

            return redirect("superadmin_services")

    else:

        form = ServiceForm()

    return render(
        request,
        "superadmin_panel/service_form.html",
        {
            "form": form,
            "title": "افزودن خدمت"
        }
    )


@login_required
def service_edit(request, id):

    service = Service.objects.get(id=id)

    if request.method == "POST":

        form = ServiceForm(
            request.POST,
            request.FILES,
            instance=service
        )

        if form.is_valid():

            form.save()

            return redirect("superadmin_services")

    else:

        form = ServiceForm(instance=service)

    return render(
        request,
        "superadmin_panel/service_form.html",
        {
            "form": form,
            "title": "ویرایش خدمت"
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

    user = CustomUser.objects.get(id=user_id)

    group = Group.objects.get(name="Admin")

    user.groups.remove(group)

    return redirect("superadmin_admins")




@login_required
def barber_blocked_times(request):

    barber = Barber.objects.get(user=request.user)

    if request.method == "POST":

        form = BarberBlockedTimeForm(request.POST)

        if form.is_valid():

            blocked = form.save(commit=False)

            blocked.barber = barber

            blocked.save()

            return redirect("barber_blocked_times")

    else:

        form = BarberBlockedTimeForm()

    blocked_times = BarberBlockedTime.objects.filter(
        barber=barber
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
        }
    )
@login_required
def delete_blocked_time(request, pk):

    item = get_object_or_404(
        BarberBlockedTime,
        id=pk,
        barber__user=request.user
    )

    item.delete()

    messages.success(
        request,
        "بازه زمانی حذف شد."
    )

    return redirect("barber_blocked_times")
@login_required
def edit_blocked_time(request, pk):
    
    barber = Barber.objects.get(user=request.user)

    blocked = get_object_or_404(
        BarberBlockedTime,
        id=pk,
        barber=barber
    )

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

            return redirect("barber_blocked_times")

    else:

        form = BarberBlockedTimeForm(
            instance=blocked
        )

    blocked_times = BarberBlockedTime.objects.filter(
        barber=barber
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
        }
    )
@login_required
def barber_walkin_reservation(request):

    barber = Barber.objects.get(user=request.user)

    if request.method == "POST":

        form = WalkInReservationForm(request.POST)

        if form.is_valid():

            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]

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


            else:

                Reservation.objects.create(

                    user=None,

                    customer_name=form.cleaned_data["customer_name"],

                    customer_phone=form.cleaned_data["customer_phone"],

                    barber=barber,

                    service=form.cleaned_data["service"],

                    date=date,

                    time=time,

                    status="approved"

                )


                messages.success(
                    request,
                    "نوبت حضوری ثبت شد."
                )


                return redirect(
                    "barber_walkin_reservation"
                )


    else:

        form = WalkInReservationForm()


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

        }

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

    orders = Order.objects.all().order_by("-created_at")

    return render(
        request,
        "superadmin_panel/orders.html",
        {
            "orders": orders,
        }
    )
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

        order.status = status

        order.save()


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