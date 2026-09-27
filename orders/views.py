from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone

from cart.models import Cart
from accounts.models import CustomerProfile
from store.models import Product
from .models import Order, OrderItem


@login_required
@transaction.atomic
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        return redirect("cart")

    items = list(
        cart.items.select_related("product")
    )

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        # Check stock before placing order
        for item in items:
            if item.quantity > item.product.stock:
                return render(
                    request,
                    "orders/checkout.html",
                    {
                        "items": items,
                        "total": total,
                        "profile": profile,
                        "error": (
                            f"Only {item.product.stock} "
                            f"units of {item.product.name} "
                            f"are available."
                        ),
                    }
                )

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            pincode=request.POST.get("pincode"),
            total_amount=total,
            payment_method="COD",
            payment_status="PENDING",
            status="PLACED",
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

            item.product.stock -= item.quantity

            item.product.save(
                update_fields=["stock"]
            )

        # Empty cart after successful order
        cart.items.all().delete()

        return redirect(
            "order_success",
            order_id=order.id
        )

    return render(
        request,
        "orders/checkout.html",
        {
            "items": items,
            "total": total,
            "profile": profile,
        }
    )


@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
            "items": order.items.select_related("product"),
        }
    )


@login_required
def order_tracking(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_tracking.html",
        {
            "order": order
        }
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )


@login_required
@transaction.atomic
def cancel_order(request, order_id):

    # Lock the order while cancelling
    order = get_object_or_404(
        Order.objects.select_for_update(),
        id=order_id,
        user=request.user
    )

    # Orders can only be cancelled before processing
    if order.status not in ["PLACED", "ACCEPTED"]:

        return render(
            request,
            "orders/cancel_order.html",
            {
                "order": order,
                "error": (
                    "This order can no longer be cancelled."
                )
            }
        )

    if request.method == "POST":

        reason = request.POST.get(
            "cancel_reason",
            ""
        ).strip()

        note = request.POST.get(
            "cancel_note",
            ""
        ).strip()

        valid_reasons = [
            "Ordered by mistake",
            "Ordered the wrong product",
            "Need to change quantity",
            "Found a better option",
            "Delivery address needs to be changed",
            "Ordered too many items",
            "Other",
        ]

        if reason not in valid_reasons:

            return render(
                request,
                "orders/cancel_order.html",
                {
                    "order": order,
                    "error": "Please select a valid cancellation reason."
                }
            )

        # Restore product stock
        order_items = OrderItem.objects.filter(
            order=order
        )

        for item in order_items:

            product = Product.objects.select_for_update().get(
                id=item.product_id
            )

            product.stock += item.quantity

            product.save(
                update_fields=["stock"]
            )

        # Update order cancellation details
        order.status = "CANCELLED"

        order.cancel_reason = reason

        order.cancel_note = note

        order.cancelled_at = timezone.now()

        order.save(
            update_fields=[
                "status",
                "cancel_reason",
                "cancel_note",
                "cancelled_at",
            ]
        )

        return redirect("my_orders")

    return render(
        request,
        "orders/cancel_order.html",
        {
            "order": order
        }
    )

def customer_care(request):
    return render(
        request,
        "orders/customer_care.html"
    )