from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from products.models import Product, ProductVariant


class Cart(models.Model):
    """Store a shopping cart for a user or anonymous session."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shopping_carts",
        blank=True,
        null=True,
    )

    session_key = models.CharField(
        max_length=40,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-updated_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(user__isnull=False),
                name="unique_cart_per_user",
            ),
            models.UniqueConstraint(
                fields=["session_key"],
                condition=~Q(session_key=""),
                name="unique_cart_per_session",
            ),
        ]

    def clean(self):
        """Ensure that every cart has exactly one owner."""

        has_user = self.user_id is not None
        has_session = bool(self.session_key)

        if has_user == has_session:
            raise ValidationError(
                "A cart must belong to either a user or a session."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_items(self):
        """Return the total quantity of all cart items."""

        return sum(
            self.items.values_list(
                "quantity",
                flat=True,
            )
        )

    @property
    def subtotal(self):
        """Return the combined value of all cart items."""

        return sum(
            (
                item.line_total
                for item in self.items.select_related("product")
            ),
            Decimal("0.00"),
        )

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"

        return f"Session cart {self.session_key}"


class CartItem(models.Model):
    """Store one selected product variant inside a cart."""

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="cart_items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "cart",
                    "variant",
                ],
                name="unique_variant_per_cart",
            )
        ]

    def clean(self):
        """Validate product, variant and stock consistency."""

        if (
            self.variant_id
            and self.product_id
            and self.variant.product_id != self.product_id
        ):
            raise ValidationError(
                {
                    "variant": (
                        "The selected variant does not belong "
                        "to this product."
                    )
                }
            )

        if self.product_id and not self.product.is_active:
            raise ValidationError(
                {
                    "product": "This product is not currently active."
                }
            )

        if self.variant_id and not self.variant.is_active:
            raise ValidationError(
                {
                    "variant": "This product variant is not active."
                }
            )

        if (
            self.variant_id
            and self.quantity > self.variant.stock
        ):
            raise ValidationError(
                {
                    "quantity": (
                        f"Only {self.variant.stock} item(s) "
                        "are available for this variant."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def unit_price(self):
        """Return the current selling price of the product."""

        return self.product.selling_price

    @property
    def line_total(self):
        """Return price multiplied by selected quantity."""

        return self.unit_price * self.quantity

    def __str__(self):
        return (
            f"{self.product.name} — "
            f"{self.variant.size} / "
            f"{self.variant.color_name} "
            f"× {self.quantity}"
        )