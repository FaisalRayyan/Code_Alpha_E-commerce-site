from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.models import CartItem
from cart.services import get_or_create_cart
from products.models import Product, ProductVariant

from .forms import CheckoutForm
from .models import Order, OrderItem


class CheckoutValidationError(Exception):
    """Abort checkout while keeping the database transaction clean."""


def _cart_items(cart):
    return (
        cart.items
        .select_related(
            "product",
            "product__category",
            "variant",
        )
        .all()
    )


def _checkout_initial(user):
    full_name = (
        f"{user.first_name} {user.last_name}"
    ).strip()

    if not full_name:
        full_name = user.username

    return {
        "recipient_name": full_name,
        "email": user.email,
        "payment_method": (
            Order.PaymentMethod.CASH_ON_DELIVERY
        ),
    }


@login_required(login_url="accounts:login")
def checkout(request):
    """Review the cart, collect delivery data and place a COD order."""

    cart = get_or_create_cart(request)
    cart_items = list(_cart_items(cart))

    if not cart_items:
        messages.error(
            request,
            "Your cart is empty. Add a product before checkout.",
        )

        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = CheckoutForm(
            request.POST,
        )
    else:
        form = CheckoutForm(
            initial=_checkout_initial(
                request.user
            )
        )

    if (
        request.method == "POST"
        and form.is_valid()
    ):
        try:
            with transaction.atomic():
                locked_items = list(
                    CartItem.objects
                    .select_for_update()
                    .select_related(
                        "product",
                        "variant",
                    )
                    .filter(
                        cart=cart,
                    )
                    .order_by("id")
                )

                if not locked_items:
                    raise CheckoutValidationError(
                        "Your cart is empty."
                    )

                product_ids = {
                    item.product_id
                    for item in locked_items
                }

                variant_ids = {
                    item.variant_id
                    for item in locked_items
                }

                locked_products = (
                    Product.objects
                    .select_for_update()
                    .filter(
                        id__in=product_ids
                    )
                    .in_bulk()
                )

                locked_variants = (
                    ProductVariant.objects
                    .select_for_update()
                    .filter(
                        id__in=variant_ids
                    )
                    .in_bulk()
                )

                checkout_lines = []
                subtotal = Decimal("0.00")

                for item in locked_items:
                    product = locked_products.get(
                        item.product_id
                    )

                    variant = locked_variants.get(
                        item.variant_id
                    )

                    if (
                        not product
                        or not product.is_active
                    ):
                        raise CheckoutValidationError(
                            (
                                f"{item.product.name} is no longer "
                                "available."
                            )
                        )

                    if (
                        not variant
                        or not variant.is_active
                        or variant.product_id
                        != product.id
                    ):
                        raise CheckoutValidationError(
                            (
                                f"The selected variant for "
                                f"{product.name} is no longer available."
                            )
                        )

                    if item.quantity > variant.stock:
                        raise CheckoutValidationError(
                            (
                                f"Only {variant.stock} item(s) of "
                                f"{product.name}, size {variant.size}, "
                                "are currently available."
                            )
                        )

                    unit_price = product.selling_price
                    line_total = (
                        unit_price
                        * item.quantity
                    )

                    subtotal += line_total

                    checkout_lines.append(
                        {
                            "cart_item": item,
                            "product": product,
                            "variant": variant,
                            "unit_price": unit_price,
                            "line_total": line_total,
                        }
                    )

                shipping_amount = Decimal("0.00")
                total = (
                    subtotal
                    + shipping_amount
                )

                order = Order.objects.create(
                    user=request.user,
                    recipient_name=(
                        form.cleaned_data[
                            "recipient_name"
                        ]
                    ),
                    phone=form.cleaned_data["phone"],
                    email=form.cleaned_data["email"],
                    address_line_1=(
                        form.cleaned_data[
                            "address_line_1"
                        ]
                    ),
                    address_line_2=(
                        form.cleaned_data[
                            "address_line_2"
                        ]
                    ),
                    city=form.cleaned_data["city"],
                    province=(
                        form.cleaned_data[
                            "province"
                        ]
                    ),
                    postal_code=(
                        form.cleaned_data[
                            "postal_code"
                        ]
                    ),
                    landmark=(
                        form.cleaned_data[
                            "landmark"
                        ]
                    ),
                    customer_note=(
                        form.cleaned_data[
                            "customer_note"
                        ]
                    ),
                    payment_method=(
                        form.cleaned_data[
                            "payment_method"
                        ]
                    ),
                    payment_status=(
                        Order.PaymentStatus.COD_PENDING
                    ),
                    fulfillment_status=(
                        Order.FulfillmentStatus.PENDING
                    ),
                    subtotal=subtotal,
                    shipping_amount=shipping_amount,
                    total=total,
                )

                for line in checkout_lines:
                    item = line["cart_item"]
                    product = line["product"]
                    variant = line["variant"]

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        variant=variant,
                        product_name=product.name,
                        product_sku=product.sku,
                        variant_sku=variant.sku,
                        size=variant.size,
                        color_name=variant.color_name,
                        color_hex=variant.color_hex,
                        unit_price=(
                            line["unit_price"]
                        ),
                        quantity=item.quantity,
                        line_total=(
                            line["line_total"]
                        ),
                    )

                    variant.stock -= item.quantity
                    variant.save(
                        update_fields=["stock"]
                    )

                    product.stock = max(
                        0,
                        product.stock
                        - item.quantity,
                    )
                    product.save(
                        update_fields=["stock"]
                    )

                cart.items.all().delete()
                cart.save(
                    update_fields=["updated_at"]
                )

        except CheckoutValidationError as error:
            messages.error(
                request,
                str(error),
            )

            return redirect(
                "orders:checkout"
            )

        messages.success(
            request,
            (
                f"Order {order.order_number} "
                "was placed successfully."
            ),
        )

        return redirect(
            "orders:order_success",
            order_number=order.order_number,
        )

    context = {
        "form": form,
        "cart": cart,
        "cart_items": cart_items,
        "shipping_amount": Decimal("0.00"),
        "estimated_total": cart.subtotal,
    }

    return render(
        request,
        "orders/checkout.html",
        context,
    )


@login_required(login_url="accounts:login")
def order_list(request):
    """Show only the signed-in customer's orders."""

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items")
    )

    return render(
        request,
        "orders/order_list.html",
        {
            "orders": orders,
        },
    )


@login_required(login_url="accounts:login")
def order_detail(
    request,
    order_number,
):
    """Display one customer-owned order."""

    order = get_object_or_404(
        Order.objects
        .prefetch_related(
            "items__product",
            "items__variant",
        ),
        order_number=order_number,
        user=request.user,
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
        },
    )


@login_required(login_url="accounts:login")
def order_success(
    request,
    order_number,
):
    """Display the post-checkout confirmation screen."""

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items"
        ),
        order_number=order_number,
        user=request.user,
    )

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
        },
    )


@login_required(login_url="accounts:login")
@require_POST
def cancel_order(
    request,
    order_number,
):
    """Cancel an eligible order and restore its variant/product stock."""

    with transaction.atomic():
        order = get_object_or_404(
            Order.objects
            .select_for_update()
            .prefetch_related(
                "items__product",
                "items__variant",
            ),
            order_number=order_number,
            user=request.user,
        )

        if not order.can_cancel:
            messages.error(
                request,
                "This order can no longer be cancelled.",
            )

            return redirect(
                "orders:order_detail",
                order_number=order.order_number,
            )

        for item in order.items.all():
            if item.variant_id:
                variant = (
                    ProductVariant.objects
                    .select_for_update()
                    .filter(id=item.variant_id)
                    .first()
                )

                if variant:
                    variant.stock += item.quantity
                    variant.save(
                        update_fields=["stock"]
                    )

            if item.product_id:
                product = (
                    Product.objects
                    .select_for_update()
                    .filter(id=item.product_id)
                    .first()
                )

                if product:
                    product.stock += item.quantity
                    product.save(
                        update_fields=["stock"]
                    )

        order.fulfillment_status = (
            Order.FulfillmentStatus.CANCELLED
        )
        order.save(
            update_fields=[
                "fulfillment_status",
                "updated_at",
            ]
        )

    messages.success(
        request,
        f"Order {order.order_number} was cancelled.",
    )

    return redirect(
        "orders:order_detail",
        order_number=order.order_number,
    )
