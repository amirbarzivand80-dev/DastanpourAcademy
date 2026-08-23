from django.shortcuts import render, get_object_or_404
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem
from core.models import ActivityLog
from django.contrib import messages
from core.offer_utils import get_product_offer_price
from django.contrib.auth.decorators import login_required
def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    related_products = product.related_products.all()

    comments = product.comments.filter(
        is_active=True
    ).order_by("-created_at")

    offer_price = get_product_offer_price(product)

    if offer_price["has_offer"]:
        final_price = offer_price["new_price"]
    elif product.discount_price:
        final_price = product.discount_price
    else:
        final_price = product.price

    return render(
        request,
        "core/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "comments": comments,
            "final_price": final_price,
            "offer_price": offer_price,
        }
    )
from django.shortcuts import render
from .models import Product

from .models import Product, Category
def shop(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    # اعمال تخفیف پیشنهاد ویژه روی محصولات
    for product in products:

        offer_price = get_product_offer_price(product)

        product.offer_has_discount = offer_price["has_offer"]
        product.offer_discount_percent = offer_price["discount_percent"]
        product.offer_old_price = offer_price["old_price"]
        product.offer_new_price = offer_price["new_price"]

    return render(
        request,
        "core/shop.html",
        {
            "products": products,
            "categories": categories,
        }
    )
@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related(
        "product"
    ).all()

    # =====================================================
    # مبلغ اصلی سبد
    # =====================================================

    total_price = sum(
        item.total_price()
        for item in items
    )

    discount_code = request.session.get(
        "discount_code"
    )

    discount_amount = 0
    final_price = total_price
    discount_error = None
    discount_success = None

    # =====================================================
    # اعمال کد تخفیف
    # =====================================================

    if request.method == "POST":

        code = request.POST.get(
            "discount_code",
            ""
        ).strip().upper()

        # پاک کردن تخفیف قبلی
        request.session.pop("discount_code", None)
        request.session.pop("discount_amount", None)
        request.session.pop("discount_final_price", None)

        discount_code = None

        if not code:

            discount_error = "کد تخفیف را وارد کنید."

        else:

            from discounts.models import DiscountCode, DiscountUsage

            try:

                discount = DiscountCode.objects.get(
                    code=code
                )

            except DiscountCode.DoesNotExist:

                discount_error = "کد تخفیف وارد شده معتبر نیست."

            else:

                # =================================================
                # اعتبار کلی
                # =================================================

                if not discount.is_valid_now():

                    discount_error = (
                        "این کد تخفیف فعال یا معتبر نیست."
                    )

                else:

                    # =================================================
                    # محدودیت کاربر
                    # =================================================

                    user_usage_count = DiscountUsage.objects.filter(
                        discount=discount,
                        user=request.user
                    ).count()

                    if (
                        discount.per_user_limit is not None
                        and user_usage_count >= discount.per_user_limit
                    ):

                        discount_error = (
                            "شما قبلاً به تعداد مجاز از این کد استفاده کرده‌اید."
                        )

                    # =================================================
                    # کاربران مجاز
                    # =================================================

                    elif (
                        discount.users.exists()
                        and not discount.users.filter(
                            id=request.user.id
                        ).exists()
                    ):

                        discount_error = (
                            "این کد تخفیف برای حساب شما قابل استفاده نیست."
                        )

                    # =================================================
                    # حداقل خرید
                    # =================================================

                    elif (
                        discount.minimum_purchase
                        and total_price < discount.minimum_purchase
                    ):

                        discount_error = (
                            f"حداقل مبلغ خرید برای این کد "
                            f"{discount.minimum_purchase:,} تومان است."
                        )

                    else:

                        # =================================================
                        # پیدا کردن محصولات مشمول
                        # =================================================

                        eligible_amount = 0

                        for item in items:

                            product = item.product

                            if discount.products_all:

                                eligible_amount += item.total_price()

                            elif discount.products.filter(
                                id=product.id
                            ).exists():

                                eligible_amount += item.total_price()

                        print(
                            "🔥 ELIGIBLE AMOUNT:",
                            eligible_amount
                        )

                        # =================================================
                        # هیچ محصولی مشمول نیست
                        # =================================================

                        if eligible_amount <= 0:

                            discount_error = (
                                "این کد تخفیف برای محصولات موجود در سبد شما قابل استفاده نیست."
                            )

                        else:

                            # =================================================
                            # محاسبه تخفیف
                            # =================================================

                            if discount.discount_type == "percent":

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

                            # =================================================
                            # مبلغ نهایی
                            # =================================================

                            final_price = max(
                                total_price - discount_amount,
                                0
                            )

                            print(
                                "🔥 TOTAL:",
                                total_price
                            )

                            print(
                                "🔥 DISCOUNT AMOUNT:",
                                discount_amount
                            )

                            print(
                                "🔥 FINAL:",
                                final_price
                            )

                            # =================================================
                            # ذخیره در Session
                            # =================================================

                            request.session[
                                "discount_code"
                            ] = discount.code

                            request.session[
                                "discount_amount"
                            ] = discount_amount

                            request.session[
                                "discount_final_price"
                            ] = final_price

                            discount_code = discount.code

                            discount_success = (
                                "کد تخفیف با موفقیت اعمال شد."
                            )

    # =====================================================
    # اگر قبلاً کد تخفیف اعمال شده
    # =====================================================

    elif discount_code:

        from discounts.models import DiscountCode

        try:

            discount = DiscountCode.objects.get(
                code=discount_code
            )

            if discount.is_valid_now():

                discount_amount = request.session.get(
                    "discount_amount",
                    0
                )

                final_price = max(
                    total_price - discount_amount,
                    0
                )

                discount_success = (
                    "کد تخفیف اعمال شده است."
                )

            else:

                request.session.pop(
                    "discount_code",
                    None
                )

                request.session.pop(
                    "discount_amount",
                    None
                )

                request.session.pop(
                    "discount_final_price",
                    None
                )

                discount_code = None

        except DiscountCode.DoesNotExist:

            request.session.pop(
                "discount_code",
                None
            )

            request.session.pop(
                "discount_amount",
                None
            )

            request.session.pop(
                "discount_final_price",
                None
            )

            discount_code = None

    # =====================================================
    # نمایش سبد
    # =====================================================

    return render(
        request,
        "core/cart.html",
        {
            "cart": cart,
            "items": items,
            "total_price": total_price,

            "discount_code": discount_code,
            "discount_amount": discount_amount,
            "final_price": final_price,

            "discount_error": discount_error,
            "discount_success": discount_success,
        }
    )
@login_required(login_url="/login/")
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart")

from django.http import JsonResponse



@login_required(login_url="/login/")
def update_cart_quantity(request, item_id):

    

    if request.method == "POST":

       

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
@login_required(login_url="/login/")
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

    # =========================================
    # مبلغ اصلی سبد
    # =========================================

    total_price = sum(
        item.total_price()
        for item in items
    )

    # =========================================
    # دریافت تخفیف از Session
    # =========================================

    discount_code = request.session.get(
        "discount_code"
    )

    discount_amount = request.session.get(
        "discount_amount",
        0
    )

    # =========================================
    # مبلغ نهایی
    # =========================================

    final_price = max(
        total_price - discount_amount,
        0
    )

    # =========================================
    # اگر کد تخفیف وجود داشت،
    # اعتبارش را دوباره بررسی کن
    # =========================================

    if discount_code:

        from discounts.models import DiscountCode

        try:

            discount = DiscountCode.objects.get(
                code=discount_code
            )

            if not discount.is_valid_now():

                discount_code = None
                discount_amount = 0
                final_price = total_price

                request.session.pop(
                    "discount_code",
                    None
                )

                request.session.pop(
                    "discount_amount",
                    None
                )

                request.session.pop(
                    "discount_final_price",
                    None
                )

        except DiscountCode.DoesNotExist:

            discount_code = None
            discount_amount = 0
            final_price = total_price

            request.session.pop(
                "discount_code",
                None
            )

            request.session.pop(
                "discount_amount",
                None
            )

            request.session.pop(
                "discount_final_price",
                None
            )

    # =========================================
    # ثبت سفارش
    # =========================================

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

        # =========================================
        # ساخت سفارش
        # =========================================

        order = Order.objects.create(

            user=request.user,

            full_name=full_name,

            phone=phone,

            postal_code=postal_code,

            address=address,

            delivery_type=delivery_type,

            receiver_name=receiver_name,

            receiver_phone=receiver_phone,

            # مبلغ نهایی تخفیف خورده
            total_price=final_price,

            status="pending",

        )

        # =========================================
        # ساخت آیتم‌های سفارش
        # =========================================

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

        # =========================================
        # ثبت استفاده از کد تخفیف
        # =========================================

        if discount_code and discount_amount > 0:

            from discounts.models import (
                DiscountCode,
                DiscountUsage
            )

            try:

                discount = DiscountCode.objects.get(
                    code=discount_code
                )

                DiscountUsage.objects.create(

                    discount=discount,

                    user=request.user,

                    discount_amount=discount_amount,

                    original_amount=total_price,

                    final_amount=final_price,

                )

                discount.used_count += 1

                discount.save(
                    update_fields=["used_count"]
                )

            except DiscountCode.DoesNotExist:

                pass

        # =========================================
        # ثبت لاگ
        # =========================================

        ActivityLog.objects.create(

            user=request.user,

            action=f"{request.user.full_name} یک سفارش جدید ثبت کرد"

        )

        # =========================================
        # پاک کردن تخفیف از Session
        # =========================================

        request.session.pop(
            "discount_code",
            None
        )

        request.session.pop(
            "discount_amount",
            None
        )

        request.session.pop(
            "discount_final_price",
            None
        )

        # =========================================
        # خالی کردن سبد
        # =========================================

        items.delete()

        return redirect("cart")

    # =========================================
    # نمایش Checkout
    # =========================================

    return render(
        request,
        "core/checkout.html",
        {
            "cart": cart,
            "items": items,

            # مبلغ اصلی
            "total_price": total_price,

            # مبلغ تخفیف
            "discount_amount": discount_amount,

            # مبلغ نهایی
            "final_price": final_price,

            # خود کد
            "discount_code": discount_code,

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