from django import forms
from django.contrib.auth.models import User


class CustomerRegistrationForm(forms.ModelForm):

    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Full Name"
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username"
    )

    email = forms.CharField(
        max_length=254,
        required=False,
        label="Email Address"
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Password"
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Confirm Password"
    )

    class Meta:

        model = User

        fields = [
            "full_name",
            "username",
            "email",
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        full_name = self.cleaned_data["full_name"].strip()

        parts = full_name.split(maxsplit=1)

        user.first_name = (
            parts[0] if parts else ""
        )

        user.last_name = (
            parts[1]
            if len(parts) > 1
            else ""
        )

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user