from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product, ProductVariant

from .models import CartItem
from .services import get_or_create_cart


def cart_detail(request):
    """Display the current customer or guest shopping cart."""

    cart = get_or_create_cart(request)

    cart_items = (
        cart.items
        .select_related(
            "product",
            "product__category",
            "variant",
        )
        .all()
    )

    context = {
        "cart": cart,
        "cart_items": cart_items,
    }

    return render(
        request,
        "cart/cart_detail.html",
        context,
    )


@require_POST
def add_to_cart(request, product_id):
    """Add a selected product variant to the current cart."""

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    variant_id = request.POST.get("variant_id")
    quantity_value = request.POST.get("quantity", "1")

    if not variant_id:
        messages.error(
            request,
            "Please select a size before adding the product.",
        )

        return redirect(
            "products:product_detail",
            slug=product.slug,
        )

    try:
        quantity = int(quantity_value)
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        messages.error(
            request,
            "Product quantity must be at least 1.",
        )

        return redirect(
            "products:product_detail",
            slug=product.slug,
        )

    variant = get_object_or_404(
        ProductVariant,
        id=variant_id,
        product=product,
        is_active=True,
    )

    if variant.stock < 1:
        messages.error(
            request,
            "This product variant is currently out of stock.",
        )

        return redirect(
            "products:product_detail",
            slug=product.slug,
        )

    if quantity > variant.stock:
        messages.error(
            request,
            (
                f"Only {variant.stock} item(s) are available "
                "for this size and color."
            ),
        )

        return redirect(
            "products:product_detail",
            slug=product.slug,
        )

    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={
            "product": product,
            "quantity": quantity,
        },
    )

    if not created:
        new_quantity = cart_item.quantity + quantity

        if new_quantity > variant.stock:
            messages.error(
                request,
                (
                    f"Your cart already contains "
                    f"{cart_item.quantity} item(s). "
                    f"Only {variant.stock} item(s) are available."
                ),
            )

            return redirect(
                "products:product_detail",
                slug=product.slug,
            )

        cart_item.quantity = new_quantity
        cart_item.save()

    cart.save(update_fields=["updated_at"])

    messages.success(
        request,
        (
            f"{product.name}, size {variant.size}, "
            "was added to your cart."
        ),
    )

    return redirect("cart:cart_detail")


@require_POST
def update_cart_item(request, item_id):
    """Increase or decrease one cart item's quantity."""

    cart = get_or_create_cart(request)

    cart_item = get_object_or_404(
        CartItem.objects.select_related(
            "product",
            "variant",
        ),
        id=item_id,
        cart=cart,
    )

    action = request.POST.get("action")

    if action == "increase":
        if cart_item.quantity >= cart_item.variant.stock:
            messages.error(
                request,
                (
                    f"Only {cart_item.variant.stock} item(s) "
                    f"of size {cart_item.variant.size} "
                    "are available."
                ),
            )

            return redirect("cart:cart_detail")

        cart_item.quantity += 1
        cart_item.save()

        messages.success(
            request,
            f"{cart_item.product.name} quantity updated.",
        )

    elif action == "decrease":
        if cart_item.quantity <= 1:
            messages.error(
                request,
                "Quantity cannot be lower than 1. Use Remove instead.",
            )

            return redirect("cart:cart_detail")

        cart_item.quantity -= 1
        cart_item.save()

        messages.success(
            request,
            f"{cart_item.product.name} quantity updated.",
        )

    else:
        messages.error(
            request,
            "Invalid cart update request.",
        )

    cart.save(update_fields=["updated_at"])

    return redirect("cart:cart_detail")


@require_POST
def remove_cart_item(request, item_id):
    """Remove one selected item from the current cart."""

    cart = get_or_create_cart(request)

    cart_item = get_object_or_404(
        CartItem.objects.select_related(
            "product",
            "variant",
        ),
        id=item_id,
        cart=cart,
    )

    product_name = cart_item.product.name
    variant_size = cart_item.variant.size

    cart_item.delete()
    cart.save(update_fields=["updated_at"])

    messages.success(
        request,
        f"{product_name}, size {variant_size}, was removed.",
    )

    return redirect("cart:cart_detail")