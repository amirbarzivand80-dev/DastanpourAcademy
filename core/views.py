from django.shortcuts import render
from shop.models import Product
from academy.models import Course
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from services.models import Service
from reservation.models import Barber
def home(request):

    products = Product.objects.filter(
        is_active=True
    ).exclude(
        slug=""
    ).order_by("-created_at")[:10]

    courses = Course.objects.filter(
        is_active=True
    ).order_by("-created_at")[:10]

    latest_products = products[:5]
    latest_courses = courses[:5]

    return render(
        request,
        "core/home.html",
        {
            "products": products,
            "courses": courses,
            "latest_products": latest_products,
            "latest_courses": latest_courses,
        }
    )

def services(request):
    return render(request, "core/services.html")
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
def education(request):
    return render(request, "core/education.html")
def course_detail(request,id):
    return render(request,"core/course_detail.html")
def shop(request):
    return render(request, "core/shop.html")
from shop.models import Product
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
def cart(request):
    return render(request,"core/cart.html")
from .models import ConsultationRequest

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
from shop.models import Favorite

@login_required(login_url="/login/")
def favorites(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related("product")


    return render(
        request,
        "core/favorites.html",
        {
            "favorites": favorites
        }
    )
def about(request):
    return render(request, "core/about.html")
from .forms import ContactMessageForm
from .forms import ContactMessageForm


def contact(request):

    if request.method == "POST":

        form = ContactMessageForm(request.POST)

        if form.is_valid():

            message = form.save(commit=False)


            if request.user.is_authenticated:

                message.user = request.user

                message.full_name = request.user.full_name

                message.phone = request.user.phone


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
def reservation(request):

    services = Service.objects.filter(
        is_active=True
    ).prefetch_related(
        "barbers__user"
    )

    selected_service_id = request.GET.get("service")

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
@login_required
@login_required
def profile_redirect(request):

    user = request.user
    print("USER:", user.full_name)
    print("IS BARBER:", user.is_barber)
    print("GROUPS:", list(user.groups.values_list("name", flat=True)))


    if user.is_superuser:
        return redirect('dashboard')

    if user.groups.filter(name__in=[
        'SuperAdmin',
        'Admin',
        'Barber'
    ]).exists():
        return redirect('dashboard')

    return redirect('profile')

from shop.forms import ProductCommentForm
from shop.models import ProductComment
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def add_comment(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )


    if request.method == "POST":

        form = ProductCommentForm(request.POST)


        if form.is_valid():

            comment = form.save(commit=False)

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

def rules(request):

    return render(
        request,
        "core/rules.html"
    )

def privacy(request):

    return render(
        request,
        "core/privacy.html"
    )