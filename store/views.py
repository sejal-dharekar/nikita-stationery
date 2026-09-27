from django.shortcuts import render, get_object_or_404
from .models import Product, Category


CATEGORY_IMAGES = {
    "Writing Supplies": "images/writingsupplies.jpg",
    "Books & Notebooks": "images/books.jpg",
    "Files & Folders": "images/files.jpg",
    "Art & Craft": "images/arts.jpg",
    "School Supplies": "images/school.jpg",
    "Office Supplies": "images/office.jpg",
}

def get_product_image(product):
    if product.image:
        return product.image.url

    return CATEGORY_IMAGES.get(
    product.category.name,
    "images/office.jpg"
)


def home(request):

    categories = Category.objects.all().order_by("name")

    featured_products = Product.objects.filter(
        is_active=True
    ).order_by("-created_at")[:8]

    for product in featured_products:
        product.display_image = get_product_image(product)

    return render(
        request,
        "store/home.html",
        {
            "categories": categories,
            "featured_products": featured_products,
        }
    )


def product_list(request):

    products = Product.objects.filter(
        is_active=True
    )

    search = request.GET.get("search")
    category_id = request.GET.get("category")

    if search:
        products = products.filter(
            name__icontains=search
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    categories = Category.objects.all().order_by("name")

    for product in products:
        product.display_image = get_product_image(product)

    return render(
        request,
        "store/products.html",
        {
            "products": products,
            "search": search,
            "categories": categories,
            "selected_category": category_id,
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(
        id=product.id
    )[:4]

    product.display_image = get_product_image(product)

    for item in related_products:
        item.display_image = get_product_image(item)

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        }
    )