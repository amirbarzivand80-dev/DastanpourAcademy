from django.urls import path
from . import views
from .views import toggle_favorite

urlpatterns = [

    path(
        "",
        views.shop,
        name="shop"
    ),

    path(
        "product/<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),
    path(
    "cart/add/<int:product_id>/",
    views.add_to_cart,
    name="add_to_cart"
),
    path(
    "cart/",
    views.cart,
    name="cart"
),
    path(
    "cart/remove/<int:item_id>/",
    views.remove_from_cart,
    name="remove_from_cart"
),
path(
    "cart/update/<int:item_id>/",
    views.update_cart_quantity,
    name="update_cart_quantity"
),
    path(
    "checkout/",
    views.checkout,
    name="checkout"
),
path(
        "favorite/<int:id>/",
        views.toggle_favorite,
        name="toggle_favorite"
    ),
]