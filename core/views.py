from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from shop.models import Product, Favorite, ProductComment
from academy.models import Course
from services.models import Service
from reservation.models import Barber

from .models import HomeOffer, ConsultationRequest
from .forms import ContactMessageForm

from core.offer_utils import (
    get_product_offer_price,
    get_course_offer_price,
)

from shop.forms import ProductCommentForm

# =====================================================
# HOME
# =====================================================

def home(request):

    # =====================================================
    # محصولات صفحه اصلی
    # =====================================================

    products = list(
        Product.objects.filter(
            is_active=True
        ).exclude(
            slug=""
        ).order_by("-created_at")[:10]
    )

    # =====================================================
    # دوره‌های صفحه اصلی
    # =====================================================

    courses = list(
        Course.objects.filter(
            is_active=True
        ).order_by("-created_at")[:10]
    )

    # =====================================================
    # جدیدترین محصولات و دوره‌ها
    # =====================================================

    latest_products = products[:5]
    latest_courses = courses[:5]

    # =====================================================
    # قیمت تخفیفی محصولات صفحه اصلی
    # =====================================================

    for product in products:

        offer_price = get_product_offer_price(product)

        print("========== HOME PRODUCT ==========")
        print("NAME:", product.name)
        print("PRICE:", product.price)
        print("DISCOUNT PRICE:", product.discount_price)
        print("OFFER:", offer_price)

        product.offer_has_discount = offer_price["has_offer"]
        product.offer_discount_percent = offer_price["discount_percent"]
        product.offer_old_price = offer_price["old_price"]
        product.offer_new_price = offer_price["new_price"]

    # =====================================================
    # قیمت تخفیفی دوره‌های صفحه اصلی
    # =====================================================

    for course in courses:

        offer_price = get_course_offer_price(course)

        course.offer_has_discount = offer_price["has_offer"]
        course.offer_discount_percent = offer_price["discount_percent"]
        course.offer_old_price = offer_price["old_price"]
        course.offer_new_price = offer_price["new_price"]

    # =====================================================
    # پیشنهاد فعال صفحه اصلی
    # =====================================================

    home_offer = HomeOffer.objects.filter(
        is_active=True,
        end_time__gt=timezone.now()
    ).order_by("-created_at").first()

    # =====================================================
    # محصولات پیشنهاد ویژه
    # =====================================================

    if home_offer:

        offer_products = list(
            home_offer.products.all()
        )

        for product in offer_products:

            offer_price = get_product_offer_price(product)

            print("========== HOME OFFER PRODUCT ==========")
            print("NAME:", product.name)
            print("PRICE:", product.price)
            print("DISCOUNT PRICE:", product.discount_price)
            print("OFFER:", offer_price)

            product.offer_has_discount = offer_price["has_offer"]
            product.offer_discount_percent = offer_price["discount_percent"]
            product.offer_old_price = offer_price["old_price"]
            product.offer_new_price = offer_price["new_price"]

        # =================================================
        # دوره‌های پیشنهاد ویژه
        # =================================================

        offer_courses = list(
            home_offer.courses.all()
        )

        for course in offer_courses:

            offer_price = get_course_offer_price(course)

            course.offer_has_discount = offer_price["has_offer"]
            course.offer_discount_percent = offer_price["discount_percent"]
            course.offer_old_price = offer_price["old_price"]
            course.offer_new_price = offer_price["new_price"]

        # =================================================
        # آماده‌سازی برای Template
        # =================================================

        home_offer.offer_products = offer_products
        home_offer.offer_courses = offer_courses

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "core/home.html",
        {
            "products": products,
            "courses": courses,
            "latest_products": latest_products,
            "latest_courses": latest_courses,
            "home_offer": home_offer,
        }
    )

# =====================================================
# SERVICES
# =====================================================

def services(request):

    return render(
        request,
        "core/services.html"
    )


def service_detail(request, id):

    service = get_object_or_404(
        Service,
        id=id,
        is_active=True
    )

    return render(
        request,
        "core/service_detail.html",
        {
            "service": service,
        }
    )


# =====================================================
# EDUCATION
# =====================================================

def education(request):

    return render(
        request,
        "core/education.html"
    )


def course_detail(request, id):

    return render(
        request,
        "core/course_detail.html"
    )


# =====================================================
# SHOP
# =====================================================

def shop(request):

    return render(
        request,
        "core/shop.html"
    )


# =====================================================
# PRODUCT DETAIL
# =====================================================

def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    related_products = product.related_products.all()

    comments = product.comments.filter(
        is_active=True
    )

    print("RELATED:", related_products)

    return render(
        request,
        "core/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "comments": comments,
        }
    )


# =====================================================
# CART
# =====================================================

def cart(request):

    return render(
        request,
        "core/cart.html"
    )


# =====================================================
# CONSULTATION
# =====================================================

def consultation(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ConsultationRequest.objects.create(
            full_name=full_name,
            phone=phone,
            subject=subject,
            message=message
        )

        return redirect("consultation")

    return render(
        request,
        "core/consultation.html"
    )


# =====================================================
# FAVORITES
# =====================================================

@login_required(login_url="/login/")
def favorites(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        "product"
    )

    return render(
        request,
        "core/favorites.html",
        {
            "favorites": favorites
        }
    )


# =====================================================
# ABOUT
# =====================================================

def about(request):

    return render(
        request,
        "core/about.html"
    )


# =====================================================
# CONTACT
# =====================================================

def contact(request):

    if request.method == "POST":

        form = ContactMessageForm(
            request.POST
        )

        if form.is_valid():

            message = form.save(
                commit=False
            )

            if request.user.is_authenticated:

                message.user = request.user

                message.full_name = (
                    request.user.full_name
                )

                message.phone = (
                    request.user.phone
                )

            message.save()

            return redirect("contact")

    else:

        form = ContactMessageForm()

    return render(
        request,
        "core/contact.html",
        {
            "form": form
        }
    )


# =====================================================
# RESERVATION
# =====================================================

def reservation(request):

    services = Service.objects.filter(
        is_active=True
    ).prefetch_related(
        "barbers__user"
    )

    selected_service_id = request.GET.get(
        "service"
    )

    selected_service = None

    if selected_service_id:

        selected_service = get_object_or_404(
            Service,
            id=selected_service_id,
            is_active=True
        )

    return render(
        request,
        "core/reservation.html",
        {
            "services": services,
            "selected_service": selected_service,
        }
    )


# =====================================================
# PROFILE REDIRECT
# =====================================================

@login_required
def profile_redirect(request):

    user = request.user

    print("USER:", user.full_name)
    print("IS BARBER:", user.is_barber)
    print(
        "GROUPS:",
        list(
            user.groups.values_list(
                "name",
                flat=True
            )
        )
    )

    if user.is_superuser:

        return redirect("dashboard")

    if user.groups.filter(
        name__in=[
            "SuperAdmin",
            "Admin",
            "Barber"
        ]
    ).exists():

        return redirect("dashboard")

    return redirect("profile")


# =====================================================
# PRODUCT COMMENT
# =====================================================

@login_required(login_url="/login/")
def add_comment(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":

        form = ProductCommentForm(
            request.POST
        )

        if form.is_valid():

            comment = form.save(
                commit=False
            )

            comment.user = request.user

            comment.product = product

            comment.is_active = False

            comment.save()

            return redirect(
                "product_detail",
                slug=product.slug
            )

    else:

        form = ProductCommentForm()

    return render(
        request,
        "core/add_comment.html",
        {
            "form": form,
            "product": product,
        }
    )


# =====================================================
# RULES
# =====================================================

def rules(request):

    return render(
        request,
        "core/rules.html"
    )


# =====================================================
# PRIVACY
# =====================================================

def privacy(request):

    return render(
        request,
        "core/privacy.html"
    )