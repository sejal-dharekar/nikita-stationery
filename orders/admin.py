from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "total_amount",
        "payment_method",
        "payment_status",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "user__username",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "user",
        "total_amount",
        "payment_method",
        "payment_status",
        "created_at",
    )

    inlines = [OrderItemInline]