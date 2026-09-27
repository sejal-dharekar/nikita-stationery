from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import CustomerRegistrationForm
from .models import CustomerProfile


def register(request):

    if request.method == "POST":

        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            CustomerProfile.objects.get_or_create(
                user=user
            )

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend"
            )

            return redirect("home")

    else:

        form = CustomerRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


@login_required
def profile(request):

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        parts = full_name.split(maxsplit=1)

        request.user.first_name = parts[0] if parts else ""
        request.user.last_name = parts[1] if len(parts) > 1 else ""

        request.user.email = request.POST.get(
            "email",
            ""
        ).strip()

        profile.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        profile.address = request.POST.get(
            "address",
            ""
        ).strip()

        profile.city = request.POST.get(
            "city",
            ""
        ).strip()

        profile.pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        request.user.save()
        profile.save()

        return redirect("profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile
        }
    )