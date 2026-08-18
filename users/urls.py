from django.urls import path
from . import views

urlpatterns = [

    path("login/", views.login_view, name="login"),

    path("register/", views.register_view, name="register"),

    path("profile/", views.profile_view, name="profile"),

    path(
    "verify-phone/",
    views.verify_phone,
    name="verify_phone"
),

    path(
        "upload-profile-image/",
        views.upload_profile_image,
        name="upload_profile_image"
    ),

    path(
        "update-profile/",
        views.update_profile,
        name="update_profile"
    ),
path(
    "profile-data/",
    views.profile_data,
    name="profile_data"
),
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),
    path(
    "my-orders/",
    views.my_orders,
    name="my_orders"
),
path(
    "order/<int:id>/",
    views.order_detail,
    name="order_detail"
),
path(
    "my-bookings/",
    views.my_bookings,
    name="my_bookings"
),
path(
    "reservation/<int:id>/",
    views.reservation_detail,
    name="reservation_detail"
),
path(
    "my-courses/",
    views.my_courses,
    name="my_courses"
),
path(
    "my-course/<int:id>/",
    views.user_course_detail,
    name="user_course_detail"
),
path(
    "session/<int:id>/",
    views.session_detail,
    name="session_detail"
),
path(
    "my-favorites/",
    views.my_favorites,
    name="my_favorites"
),
path(
    "change-password/",
    views.change_password,
    name="change_password"
),
]