import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create or update the demo owner account"

    def handle(self, *args, **options):
        username = os.environ.get("OWNER_USERNAME")
        email = os.environ.get("OWNER_EMAIL")
        password = os.environ.get("OWNER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Owner environment variables not configured."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email or "",
            },
        )

        user.email = email or ""
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Owner '{username}' created successfully."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Owner '{username}' updated successfully."
                )
            )