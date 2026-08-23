from django.utils import timezone

from .models import HomeOffer


def get_product_offer_price(product):

    now = timezone.now()

    offer = HomeOffer.objects.filter(
        products=product,
        is_active=True,
        end_time__gt=now,
    ).order_by("-created_at").first()

    if not offer:
        return {
            "has_offer": False,
            "discount_percent": 0,
            "old_price": None,
            "new_price": product.price,
        }

    discount_percent = offer.discount_percent

    if discount_percent <= 0:
        return {
            "has_offer": False,
            "discount_percent": 0,
            "old_price": None,
            "new_price": product.price,
        }

    new_price = round(
        product.price * (100 - discount_percent) / 100
    )

    return {
        "has_offer": True,
        "discount_percent": discount_percent,
        "old_price": product.price,
        "new_price": new_price,
    }


def get_course_offer_price(course):

    now = timezone.now()

    offer = HomeOffer.objects.filter(
        courses=course,
        is_active=True,
        end_time__gt=now,
    ).order_by("-created_at").first()

    if not offer:
        return {
            "has_offer": False,
            "discount_percent": 0,
            "old_price": None,
            "new_price": course.price,
        }

    discount_percent = offer.discount_percent

    if discount_percent <= 0:
        return {
            "has_offer": False,
            "discount_percent": 0,
            "old_price": None,
            "new_price": course.price,
        }

    new_price = round(
        course.price * (100 - discount_percent) / 100
    )

    return {
        "has_offer": True,
        "discount_percent": discount_percent,
        "old_price": course.price,
        "new_price": new_price,
    }


def get_final_product_price(product):

    # تخفیف دستی محصول
    if product.discount_price is not None:
        return product.discount_price

    # پیشنهاد ویژه
    offer_price = get_product_offer_price(product)

    if offer_price["has_offer"]:
        return offer_price["new_price"]

    # قیمت عادی
    return product.price