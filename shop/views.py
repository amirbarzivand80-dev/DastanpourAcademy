from django.shortcuts import render, get_object_or_404
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem
from core.models import ActivityLog
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
@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    items = cart.items.all()

    total_price = sum(
        item.total_price()
        for item in items
    )

    if request.method == "POST":

        order = Order.objects.create(

            user=request.user,

            full_name=request.POST.get("full_name"),

            phone=request.POST.get("phone"),

            address=request.POST.get("address"),

            total_price=total_price,

        )
        ActivityLog.objects.create(
         user=request.user,
         action=f"{request.user.full_name} یک سفارش جدید ثبت کرد"
)

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

        items.delete()

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