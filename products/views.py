from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    """Display all active ShopSphere products."""

    products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category")
        .prefetch_related("variants")
    )

    context = {
        "products": products,
    }

    return render(
        request,
        "products/product_list.html",
        context,
    )


def product_detail(request, slug):
    """Display one active product and its related information."""

    product = get_object_or_404(
        Product.objects
        .select_related("category")
        .prefetch_related(
            "images",
            "variants",
        ),
        slug=slug,
        is_active=True,
    )

    related_products = (
        Product.objects
        .filter(
            category=product.category,
            is_active=True,
        )
        .exclude(id=product.id)[:4]
    )

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(
        request,
        "products/product_detail.html",
        context,
    )