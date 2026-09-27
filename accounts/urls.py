from django.urls import path

from .views import (
    register,
    profile,
)


urlpatterns = [

    path(
        "",
        register,
        name="register"
    ),

    path(
        "profile/",
        profile,
        name="profile"
    ),

]