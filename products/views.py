from django.shortcuts import render

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