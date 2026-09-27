from django.contrib import admin
from django.urls import path, include

from accounts.views import register
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),

    path("register/", register, name="register"),

    path(
    "account/",
    include("accounts.urls")
     ),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login",
    ),


    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    path(
    "",
    include("store.urls")
),

    path(
        "cart/",
        include("cart.urls")
    ),

    path(
        "orders/",
        include("orders.urls")
    ),

    path(
        "dashboard/",
        include("dashboard.urls")
    ),
]


# Product image/media support during development
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)