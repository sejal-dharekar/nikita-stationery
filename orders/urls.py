from django.urls import path

from .views import (
    checkout,
    order_success,
    order_tracking,
    my_orders,
    customer_care,
    cancel_order,
)


urlpatterns = [
    path(
        "checkout/",
        checkout,
        name="checkout"
    ),

    path(
        "success/<int:order_id>/",
        order_success,
        name="order_success"
    ),

    path(
        "track/<int:order_id>/",
        order_tracking,
        name="order_tracking"
    ),

    path(
        "my-orders/",
        my_orders,
        name="my_orders"
    ),

    path(
        "cancel/<int:order_id>/",
        cancel_order,
        name="cancel_order"
    ),

    path(
        "customer-care/",
        customer_care,
        name="customer_care"
    ),
]