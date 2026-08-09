from django.shortcuts import render, get_object_or_404
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem
from core.models import ActivityLog
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )


    related_products = product.related_products.all()


    comments = product.comments.filter(
        is_active=True
    ).order_by(
        "-created_at"
    )


    return render(
        request,
        "core/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "comments": comments,
        }
    )

from django.shortcuts import render
from .models import Product

from .models import Product, Category
def shop(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    return render(
        request,
        "core/shop.html",
        {
            "products": products,
            "categories": categories,
        }
    )

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart")

@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()

    total_price = sum(
        item.total_price()
        for item in items
    )

    return render(
        request,
        "core/cart.html",
        {
            "cart": cart,
            "items": items,
            "total_price": total_price,
        }
    )
@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart")

from django.http import JsonResponse



@login_required
def update_cart_quantity(request, item_id):

    print("UPDATE CART START")

    if request.method == "POST":

        print(request.POST)

        item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        quantity = int(request.POST.get("quantity"))

        item.quantity = quantity
        item.save()

        print("SAVED:", item.quantity)

        return JsonResponse({
            "success": True
        })
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    items = cart.items.select_related(
        "product"
    ).all()

    if not items.exists():

        return redirect("cart")

    total_price = sum(
        item.total_price()
        for item in items
    )

    if request.method == "POST":

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        postal_code = request.POST.get(
            "postal_code",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        delivery_type = request.POST.get(
            "delivery_type",
            "self"
        )

        receiver_name = request.POST.get(
            "receiver_name",
            ""
        ).strip()

        receiver_phone = request.POST.get(
            "receiver_phone",
            ""
        ).strip()

        # -----------------------------
        # بررسی اطلاعات ضروری
        # -----------------------------

        if not full_name:
            messages.error(
                request,
                "نام و نام خانوادگی را وارد کنید."
            )
            return redirect("checkout")

        if not phone:
            messages.error(
                request,
                "شماره تلفن را وارد کنید."
            )
            return redirect("checkout")

        if not postal_code:
            messages.error(
                request,
                "کد پستی را وارد کنید."
            )
            return redirect("checkout")

        if not address:
            messages.error(
                request,
                "آدرس را وارد کنید."
            )
            return redirect("checkout")

        # -----------------------------
        # بررسی تحویل گیرنده
        # -----------------------------

        if delivery_type == "other":

            if not receiver_name:
                messages.error(
                    request,
                    "نام تحویل‌گیرنده را وارد کنید."
                )
                return redirect("checkout")

            if not receiver_phone:
                messages.error(
                    request,
                    "شماره تحویل‌گیرنده را وارد کنید."
                )
                return redirect("checkout")

        else:

            receiver_name = ""
            receiver_phone = ""

        # -----------------------------
        # ساخت سفارش
        # -----------------------------

        order = Order.objects.create(

            user=request.user,

            full_name=full_name,

            phone=phone,

            postal_code=postal_code,

            address=address,

            delivery_type=delivery_type,

            receiver_name=receiver_name,

            receiver_phone=receiver_phone,

            total_price=total_price,

            status="pending",

        )

        # -----------------------------
        # ساخت آیتم‌های سفارش
        # -----------------------------

        for item in items:

            if item.product.discount_price:
                price = item.product.discount_price
            else:
                price = item.product.price

            OrderItem.objects.create(

                order=order,

                product=item.product,

                quantity=item.quantity,

                price=price,

            )

        # -----------------------------
        # ثبت لاگ
        # -----------------------------

        ActivityLog.objects.create(

            user=request.user,

            action=f"{request.user.full_name} یک سفارش جدید ثبت کرد"

        )

        # -----------------------------
        # فعلاً سبد خرید خالی شود
        # -----------------------------

        items.delete()

        # فعلاً برگرد به سبد خرید
        return redirect("cart")

    return render(
        request,
        "core/checkout.html",
        {
            "cart": cart,
            "items": items,
            "total_price": total_price,
            "user": request.user,
        }
    )

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Favorite




@login_required(login_url="/login/")
def toggle_favorite(request, id):

    print("FAVORITE VIEW RUN")

    product = Product.objects.get(id=id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    print("CREATED:", created)

    if not created:
        favorite.delete()

        return JsonResponse({
            "status": "removed"
        })

    return JsonResponse({
        "status": "added"
    })