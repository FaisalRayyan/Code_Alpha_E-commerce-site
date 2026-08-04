from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Represent a product category such as Running or Lifestyle."""

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Represent a jogger or sneaker available in ShopSphere."""

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    name = models.CharField(
        max_length=180,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
    )

    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="SKU",
    )

    short_description = models.CharField(
        max_length=250,
        blank=True,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
        ],
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    main_image = models.ImageField(
        upload_to="products/main/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    is_new_arrival = models.BooleanField(
        default=False,
    )

    is_best_seller = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if (
            self.discount_price is not None
            and self.discount_price >= self.price
        ):
            raise ValidationError(
                {
                    "discount_price": (
                        "Discount price must be lower than the regular price."
                    )
                }
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.name}-{self.sku}"
            )

        super().save(*args, **kwargs)

    @property
    def selling_price(self):
        if self.discount_price is not None:
            return self.discount_price

        return self.price

    @property
    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Store additional images for a product gallery."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="products/gallery/",
    )

    alt_text = models.CharField(
        max_length=180,
        blank=True,
    )

    display_order = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.product.name} image"


class ProductVariant(models.Model):
    """Store size, color and stock combinations for a product."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
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
        help_text="Example: #000000",
    )

    sku = models.CharField(
        max_length=70,
        unique=True,
        verbose_name="Variant SKU",
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["product", "size", "color_name"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product",
                    "size",
                    "color_name",
                ],
                name="unique_product_size_color",
            )
        ]

    def __str__(self):
        return (
            f"{self.product.name} — "
            f"{self.size} / {self.color_name}"
        )