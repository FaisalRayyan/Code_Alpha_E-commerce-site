import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from products.models import Product, ProductVariant


def generate_order_number():
    """Return a compact, collision-resistant ShopSphere order number."""

    date_part = timezone.now().strftime("%Y%m%d")
    random_part = uuid.uuid4().hex[:8].upper()

    return f"SS-{date_part}-{random_part}"


class Order(models.Model):
    """Store one completed ShopSphere checkout."""

    class PaymentMethod(models.TextChoices):
        CASH_ON_DELIVERY = "cod", "Cash on Delivery"

    class PaymentStatus(models.TextChoices):
        COD_PENDING = "cod_pending", "COD Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    class FulfillmentStatus(models.TextChoices):
        PENDING = "pending", "Pending confirmation"
        CONFIRMED = "confirmed", "Confirmed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    order_number = models.CharField(
        max_length=40,
        unique=True,
        default=generate_order_number,
        editable=False,
        db_index=True,
    )

    fulfillment_status = models.CharField(
        max_length=20,
        choices=FulfillmentStatus.choices,
        default=FulfillmentStatus.PENDING,
        db_index=True,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH_ON_DELIVERY,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.COD_PENDING,
        db_index=True,
    )

    recipient_name = models.CharField(
        max_length=160,
    )

    phone = models.CharField(
        max_length=30,
    )

    email = models.EmailField(
        blank=True,
    )

    address_line_1 = models.CharField(
        max_length=220,
    )

    address_line_2 = models.CharField(
        max_length=220,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
    )

    province = models.CharField(
        max_length=60,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    landmark = models.CharField(
        max_length=160,
        blank=True,
    )

    customer_note = models.TextField(
        blank=True,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    shipping_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    @property
    def total_items(self):
        return sum(
            self.items.values_list(
                "quantity",
                flat=True,
            )
        )

    @property
    def can_cancel(self):
        return (
            self.fulfillment_status
            in {
                self.FulfillmentStatus.PENDING,
                self.FulfillmentStatus.CONFIRMED,
            }
        )

    @property
    def full_delivery_address(self):
        parts = [
            self.address_line_1,
            self.address_line_2,
            self.landmark,
            self.city,
            self.province,
            self.postal_code,
        ]

        return ", ".join(
            part
            for part in parts
            if part
        )

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    """Preserve the exact product/variant data used at checkout."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="order_items",
        blank=True,
        null=True,
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        related_name="order_items",
        blank=True,
        null=True,
    )

    product_name = models.CharField(
        max_length=180,
    )

    product_sku = models.CharField(
        max_length=50,
    )

    variant_sku = models.CharField(
        max_length=70,
    )

    size = models.CharField(
        max_length=20,
    )

    color_name = models.CharField(
        max_length=60,
    )

    color_hex = models.CharField(
        max_length=7,
        blank=True,
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()

    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return (
            f"{self.product_name} "
            f"× {self.quantity}"
        )
