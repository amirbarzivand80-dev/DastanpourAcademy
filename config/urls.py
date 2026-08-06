"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core.views import home,  education, course_detail, shop, product_detail,cart,favorites,about,contact
from users.views import logout_view, profile_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from shop.views import shop, product_detail
from core.views import home, education, course_detail, shop, product_detail,cart,favorites,about,contact,profile_redirect,rules
from core import views
from core.views import privacy
urlpatterns = [
    path('', home),
   
    path("education/" ,education,name="education"),
    path("education/course/<int:id>", course_detail, name="course_detail"),
    path(
    "shop/",
    include("shop.urls")
),
    
    path("favorites/", favorites, name="favorites"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path(
    "rules/",
    rules,
    name="rules"
),
    path("", include("users.urls")),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path(
    "profile-redirect/",
    profile_redirect,
    name="profile_redirect"
),
    path("reservation/", include("reservation.urls")),
    path("services/", include("services.urls")),
    path(
    "superadmin/",
    include("superadmin_panel.urls")
    ),
    path(
    "academy/",
    include("academy.urls"),
),

    path("admin/", admin.site.urls),
    path(
    "product/<int:id>/comment/",
    views.add_comment,
    name="add_comment"
),
path(
    "privacy/",
    privacy,
    name="privacy"
),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)