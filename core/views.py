from django.shortcuts import render

from products.models import Product


def home(request):
    """Display the ShopSphere home page with live featured products."""

    products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            "variants",
            "images",
        )
    )

    featured_products = list(
        products
        .filter(is_featured=True)[:4]
    )

    if len(featured_products) < 4:
        selected_ids = [
            product.id
            for product in featured_products
        ]

        additional_products = list(
            products
            .exclude(id__in=selected_ids)
            .order_by(
                "-is_best_seller",
                "-is_new_arrival",
                "-created_at",
            )[: 4 - len(featured_products)]
        )

        featured_products.extend(
            additional_products
        )

    context = {
        "featured_products": featured_products,
    }

    return render(
        request,
        "core/home.html",
        context,
    )
