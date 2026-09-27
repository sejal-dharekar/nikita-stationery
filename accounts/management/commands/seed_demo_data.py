from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = "Create demo categories and products"

    def handle(self, *args, **options):

        categories = [
            ("Writing Supplies", "Pens, pencils and writing essentials"),
            ("Books & Notebooks", "Books, notebooks and study materials"),
            ("School Supplies", "Essential school stationery"),
            ("Art & Craft", "Art and craft materials"),
            ("Office Supplies", "Office and workplace stationery"),
        ]

        category_objects = {}

        for name, description in categories:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={"description": description},
            )

            category_objects[name] = category

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {name}")
                )
            else:
                self.stdout.write(f"Category already exists: {name}")

        products = [
            ("Ball Pen", "Smooth writing ball pen", 5, 110, "Writing Supplies"),
            ("Classmate Book", "Classmate notebook for school and college", 50, 60, "Books & Notebooks"),
            ("Panda Pen", "Cute panda design pen", 10, 100, "Writing Supplies"),
        ]

        for name, description, price, stock, category_name in products:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "category": category_objects[category_name],
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created product: {name}")
                )
            else:
                self.stdout.write(f"Product already exists: {name}")

        self.stdout.write(
            self.style.SUCCESS("Demo categories and products are ready!")
        )