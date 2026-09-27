from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ("PLACED", "Placed"),
        ("ACCEPTED", "Accepted"),
        ("PROCESSING", "Processing"),
        ("PACKED", "Packed"),
        ("SHIPPED", "Shipped"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=30,
        default="COD"
    )

    payment_status = models.CharField(
        max_length=30,
        default="PENDING"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="PLACED"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Cancellation details
    cancel_reason = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    cancel_note = models.TextField(
        blank=True,
        null=True
    )

    cancelled_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"