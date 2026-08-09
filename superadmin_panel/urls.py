from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="superadmin_dashboard"
    ),

    path(
        "users/",
        views.users_list,
        name="superadmin_users"
    ),

    path(
        "users/<int:id>/",
        views.user_detail,
        name="superadmin_user_detail"
    ),

    path(
        "users/<int:id>/edit/",
        views.user_edit,
        name="superadmin_user_edit"
    ),
    path(
    "users/<int:user_id>/gallery/add/",
    views.customer_gallery_add,
    name="customer_gallery_add"
),

path(
    "users/gallery/<int:image_id>/delete/",
    views.customer_gallery_delete,
    name="customer_gallery_delete"
),

path(
    "users/<int:user_id>/gallery/add/",
    views.customer_gallery_add,
    name="customer_gallery_add",
),

path(
    "users/gallery/delete/<int:image_id>/",
    views.customer_gallery_delete,
    name="customer_gallery_delete",
),

    path(
    "users/delete/<int:id>/",
    views.superadmin_user_delete,
    name="superadmin_user_delete"
),
    path(
        "barbers/",
        views.barbers_list,
        name="superadmin_barbers"
    ),

    # صفحه جستجوی افزودن آرایشگر
    path(
        "barbers/add-user/",
        views.barber_search,
        name="superadmin_barber_search"
    ),
path(
    "barbers/<int:id>/edit/",
    views.barber_edit,
    name="superadmin_barber_edit"
),
path(
    "barbers/<int:id>/delete/",
    views.barber_delete,
    name="superadmin_barber_delete"
),
    # جستجوی Ajax کاربران
    path(
        "search-users/",
        views.search_users,
        name="superadmin_search_users"
    ),

    # فرم ثبت آرایشگر بعد از انتخاب کاربر
    path(
        "barbers/add/<int:user_id>/",
        views.barber_add,
        name="superadmin_barber_add"
    ),
path(
    "reservations/",
    views.reservations_list,
    name="superadmin_reservations",
),





path(
    "reservations/<int:id>/status/",
    views.reservation_status,
    name="superadmin_reservation_status",
),

path(
    "reservations/<int:id>/delete/",
    views.reservation_delete,
    name="superadmin_reservation_delete",
),

path(
    "services/",
    views.services_list,
    name="superadmin_services",
),

path(
    "services/add/",
    views.service_add,
    name="superadmin_service_add",
),

path(
    "services/<int:id>/edit/",
    views.service_edit,
    name="superadmin_service_edit",
),

path(
    "services/<int:id>/delete/",
    views.service_delete,
    name="superadmin_service_delete",
),

path(
    "admins/",
    views.admins_list,
    name="superadmin_admins",
),
path(
    "admins/<int:user_id>/permissions/",
    views.admin_permission,
    name="superadmin_admin_permission",
),
path(
    "admins/add/<int:user_id>/",
    views.admin_add,
    name="superadmin_admin_add",
),
path(
    "admins/add-user/",
    views.admin_search,
    name="superadmin_admin_search",
),
path(
    "search-admin-users/",
    views.search_admin_users,
    name="superadmin_search_admin_users",
),
path(
    "admins/remove/<int:user_id>/",
    views.admin_remove,
    name="superadmin_admin_remove",
),
path(
    "barber/blocked-times/",
    views.barber_blocked_times,
    name="barber_blocked_times",
),
path(
    "barber/blocked-time/delete/<int:pk>/",
    views.delete_blocked_time,
    name="delete_blocked_time",
),

path(
    "barber/blocked-time/edit/<int:pk>/",
    views.edit_blocked_time,
    name="edit_blocked_time",
),
path(
    "barber/walkin/",
    views.barber_walkin_reservation,
    name="barber_walkin_reservation",
),
path(
    "barber-walkin/busy-times/",
    views.barber_walkin_busy_times,
    name="barber_walkin_busy_times"
),

# ---------------- Academy ----------------

path(
    "academy/courses/",
    views.academy_courses,
    name="academy_courses",
),

path(
    "academy/courses/add/",
    views.academy_course_add,
    name="academy_course_add",
),

path(
    "academy/courses/edit/<int:pk>/",
    views.academy_course_edit,
    name="academy_course_edit",
),

path(
    "academy/courses/delete/<int:pk>/",
    views.academy_course_delete,
    name="academy_course_delete",
),
path(
    "academy/courses/<int:pk>/students/",
    views.course_students,
    name="academy_course_students",
),

path(
    "academy/students/",
    views.all_course_students,
    name="academy_all_students",
),
path(
    "academy/courses/<int:pk>/topics/",
    views.course_topics,
    name="academy_course_topics",
),
path(
    "academy/courses/<int:pk>/sessions/",
    views.course_sessions,
    name="academy_course_sessions",
),
path(
    "academy/courses/<int:pk>/sessions/add/",
    views.add_course_session,
    name="academy_add_course_session",
),
path(
    "academy/sessions/<int:session_id>/edit/",
    views.edit_course_session,
    name="academy_edit_course_session",
),
path(
    "academy/sessions/<int:session_id>/delete/",
    views.delete_course_session,
    name="academy_delete_course_session",
),
path(
    "academy/courses/<int:pk>/features/",
    views.course_features,
    name="academy_course_features",
),
path(
    "academy/courses/<int:pk>/features/add/",
    views.add_course_feature,
    name="academy_add_course_feature",
),
path(
    "academy/courses/<int:pk>/manage/",
    views.course_manage,
    name="academy_course_manage",
),
path(
    "academy/features/<int:feature_id>/edit/",
    views.edit_course_feature,
    name="academy_edit_course_feature",
),
path(
    "academy/features/<int:feature_id>/delete/",
    views.delete_course_feature,
    name="academy_delete_course_feature",
),
path(
    "academy/courses/<int:pk>/gallery/",
    views.course_gallery,
    name="academy_course_gallery",
),
path(
    "academy/courses/<int:pk>/gallery/add/",
    views.add_course_gallery,
    name="academy_add_course_gallery",
),
path(
    "academy/gallery/<int:image_id>/delete/",
    views.delete_course_gallery,
    name="academy_delete_course_gallery",
),
path(
    "products/",
    views.products,
    name="products",
),
path(
    "products/add/",
    views.add_product,
    name="add_product",
),
path(
    "products/<int:product_id>/edit/",
    views.edit_product,
    name="edit_product",
),
path(
    "products/<int:product_id>/gallery/",
    views.product_gallery,
    name="product_gallery",
),
path(
    "categories/",
    views.categories,
    name="categories",
),
path(
    "categories/add/",
    views.add_category,
    name="add_category",
),
path(
    "shop-management/",
    views.shop_management,
    name="shop_management",
),

path("brands/", views.brands, name="brands"),

path("add-brand/", views.add_brand, name="add_brand"),
path(
    "delete-brand/<int:brand_id>/",
    views.delete_brand,
    name="delete_brand"
),
path(
    "edit-brand/<int:brand_id>/",
    views.edit_brand,
    name="edit_brand"
),
path(
    "product/<int:product_id>/specifications/",
    views.product_specifications,
    name="product_specifications"
),

path(
    "product/<int:product_id>/features/",
    views.product_features,
    name="product_features"
),
path(
    "orders/",
    views.orders,
    name="orders"
),
path(
    "orders/<int:id>/",
    views.order_detail,
    name="order_detail"
),
path(
    "orders/<int:id>/update-status/",
    views.update_order_status,
    name="update_order_status"
),

path(
    "settings/",
    views.superadmin_settings,
    name="superadmin_settings"
),
path(
    "settings/change-password/",
    views.superadmin_change_password,
    name="superadmin_change_password"
),
path(
    "messages/",
    views.contact_messages,
    name="contact_messages",
),
path(
    "messages/<int:id>/",
    views.contact_message_detail,
    name="contact_message_detail"
),
path(
    "messages/<int:id>/delete/",
    views.contact_message_delete,
    name="contact_message_delete"
),
path(
    "comments/",
    views.comments,
    name="superadmin_comments"
),
path(
    "comments/activate/<int:id>/",
    views.activate_comment,
    name="activate_comment"
),


path(
    "comments/deactivate/<int:id>/",
    views.deactivate_comment,
    name="deactivate_comment"
),


path(
    "comments/delete/<int:id>/",
    views.delete_comment,
    name="delete_comment"
),
path(
    "reports/",
    views.reports,
    name="reports",
),

path(
    "products/gallery/delete/<int:image_id>/",
    views.delete_product_image,
    name="delete_product_image"
),
]
