from django.urls import path

from .views import (
    dashboard_home,
    manage_orders,
    order_detail,
    update_order_status,
    manage_products,
    add_product,
    edit_product,
    manage_categories,
    add_category,
    edit_category,
    delete_category,
    inventory,
    dashboard_customer_care,
    dashboard_settings,
)


urlpatterns = [

    path(
        "",
        dashboard_home,
        name="dashboard"
    ),

    path(
        "orders/",
        manage_orders,
        name="manage_orders"
    ),

    path(
        "orders/<int:order_id>/",
        order_detail,
        name="order_detail"
    ),

    path(
        "orders/<int:order_id>/status/",
        update_order_status,
        name="update_order_status"
    ),

    path(
        "products/",
        manage_products,
        name="manage_products"
    ),

    path(
        "products/add/",
        add_product,
        name="add_product"
    ),

    path(
        "products/<int:product_id>/edit/",
        edit_product,
        name="edit_product"
    ),

    path(
        "categories/",
        manage_categories,
        name="manage_categories"
    ),

    path(
        "categories/add/",
        add_category,
        name="add_category"
    ),

    path(
        "categories/<int:category_id>/edit/",
        edit_category,
        name="edit_category"
    ),

    path(
        "categories/<int:category_id>/delete/",
        delete_category,
        name="delete_category"
    ),

    # INVENTORY
    path(
        "inventory/",
        inventory,
        name="inventory"
    ),

    # CUSTOMER CARE
path(
    "customer-care/",
    dashboard_customer_care,
    name="dashboard_customer_care"
),


    # SETTINGS
    path(
        "settings/",
        dashboard_settings,
        name="dashboard_settings"
    ),

]