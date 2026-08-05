from .models import Cart


def cart_summary(request):
    """Provide the current cart quantity to every template."""

    if request.user.is_authenticated:
        cart = (
            Cart.objects
            .filter(user=request.user)
            .prefetch_related("items")
            .first()
        )
    else:
        session_key = request.session.session_key

        if not session_key:
            return {
                "global_cart": None,
                "global_cart_count": 0,
            }

        cart = (
            Cart.objects
            .filter(session_key=session_key)
            .prefetch_related("items")
            .first()
        )

    if not cart:
        return {
            "global_cart": None,
            "global_cart_count": 0,
        }

    total_items = sum(
        item.quantity
        for item in cart.items.all()
    )

    return {
        "global_cart": cart,
        "global_cart_count": total_items,
    }