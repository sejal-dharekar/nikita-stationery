from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

from orders.models import Order
from store.models import Product, Category


@staff_member_required
def dashboard_home(request):

    total_orders = Order.objects.count()

    placed_orders = Order.objects.filter(
        status="PLACED"
    ).count()

    delivered_orders = Order.objects.filter(
        status="DELIVERED"
    ).count()

    pending_orders = Order.objects.exclude(
        status__in=["DELIVERED", "CANCELLED"]
    ).count()

    total_sales = Order.objects.filter(
        status="DELIVERED"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    low_stock = Product.objects.filter(
        stock__lte=10,
        is_active=True
    ).order_by("stock")

    recent_orders = Order.objects.order_by(
        "-created_at"
    )[:8]

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "total_orders": total_orders,
            "placed_orders": placed_orders,
            "delivered_orders": delivered_orders,
            "pending_orders": pending_orders,
            "total_sales": total_sales,
            "low_stock": low_stock,
            "recent_orders": recent_orders,
        }
    )


@staff_member_required
def manage_orders(request):

    orders = Order.objects.select_related(
        "user"
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/manage_orders.html",
        {
            "orders": orders,
        }
    )


@staff_member_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        id=order_id
    )

    return render(
        request,
        "dashboard/order_detail.html",
        {
            "order": order,
        }
    )


@staff_member_required
def update_order_status(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        valid_statuses = [
            choice[0]
            for choice in Order.STATUS_CHOICES
        ]

        if new_status in valid_statuses:

            order.status = new_status
            order.save()

    return redirect("manage_orders")


@staff_member_required
def manage_products(request):

    products = Product.objects.select_related(
        "category"
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/manage_products.html",
        {
            "products": products,
        }
    )


@staff_member_required
def add_product(request):

    categories = Category.objects.all().order_by("name")

    if request.method == "POST":

        Product.objects.create(
            category_id=request.POST.get("category"),
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            image=request.FILES.get("image"),
            is_active=True,
        )

        return redirect("manage_products")

    return render(
        request,
        "dashboard/add_product.html",
        {
            "categories": categories,
        }
    )


@staff_member_required
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    categories = Category.objects.all().order_by("name")

    if request.method == "POST":

        product.category_id = request.POST.get("category")
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.is_active = "is_active" in request.POST

        product.save()

        return redirect("manage_products")

    return render(
        request,
        "dashboard/edit_product.html",
        {
            "product": product,
            "categories": categories,
        }
    )


@staff_member_required
def manage_categories(request):

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "dashboard/manage_categories.html",
        {
            "categories": categories,
        }
    )


@staff_member_required
def add_category(request):

    if request.method == "POST":

        Category.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )

        return redirect("manage_categories")

    return render(
        request,
        "dashboard/add_category.html"
    )


@staff_member_required
def edit_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":

        category.name = request.POST.get("name")
        category.description = request.POST.get("description")

        category.save()

        return redirect("manage_categories")

    return render(
        request,
        "dashboard/edit_category.html",
        {
            "category": category,
        }
    )


@staff_member_required
def delete_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":

        category.delete()

    return redirect("manage_categories")


# -------------------------------------------------
# INVENTORY
# -------------------------------------------------

@staff_member_required
def inventory(request):

    products = Product.objects.select_related(
        "category"
    ).order_by("stock", "name")

    return render(
        request,
        "dashboard/inventory.html",
        {
            "products": products
        }
    )


# -------------------------------------------------
# CUSTOMER CARE
# -------------------------------------------------

@staff_member_required
def dashboard_customer_care(request):

    total_orders = Order.objects.count()

    pending_orders = Order.objects.exclude(
        status__in=["DELIVERED", "CANCELLED"]
    ).count()

    delivered_orders = Order.objects.filter(
        status="DELIVERED"
    ).count()

    return render(
        request,
        "dashboard/customer_care.html",
        {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "delivered_orders": delivered_orders,
        }
    )


# -------------------------------------------------
# SETTINGS
# -------------------------------------------------

@staff_member_required
def dashboard_settings(request):

    return render(
        request,
        "dashboard/settings.html"
    )