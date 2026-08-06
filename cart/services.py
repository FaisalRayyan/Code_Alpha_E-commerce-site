from django.db import transaction

from .models import Cart, CartItem


def get_or_create_cart(request):
    """Return the authenticated user's or guest visitor's cart."""

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
        )

        return cart

    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(
        session_key=request.session.session_key,
    )

    return cart


@transaction.atomic
def merge_guest_cart_into_user(guest_session_key, user):
    """Merge an anonymous session cart into a customer cart."""

    user_cart, _ = Cart.objects.get_or_create(
        user=user,
    )

    if not guest_session_key:
        return user_cart

    guest_cart = (
        Cart.objects
        .filter(session_key=guest_session_key)
        .prefetch_related(
            "items__product",
            "items__variant",
        )
        .first()
    )

    if not guest_cart:
        return user_cart

    for guest_item in guest_cart.items.all():
        product = guest_item.product
        variant = guest_item.variant

        if (
            not product.is_active
            or not variant.is_active
            or variant.stock < 1
        ):
            continue

        user_item = (
            CartItem.objects
            .filter(
                cart=user_cart,
                variant=variant,
            )
            .first()
        )

        if user_item:
            user_item.quantity = min(
                user_item.quantity + guest_item.quantity,
                variant.stock,
            )
            user_item.save()
        else:
            CartItem.objects.create(
                cart=user_cart,
                product=product,
                variant=variant,
                quantity=min(
                    guest_item.quantity,
                    variant.stock,
                ),
            )

    guest_cart.delete()

    user_cart.save(
        update_fields=["updated_at"],
    )

    return user_cart