from django.contrib import admin

from .models import Category, Product, ProductImage, ProductVariant


class ProductImageInline(admin.TabularInline):
    """Allow product gallery images to be managed inside a product."""

    model = ProductImage
    extra = 1
    fields = (
        "image",
        "alt_text",
        "display_order",
    )


class ProductVariantInline(admin.TabularInline):
    """Allow product size and color variants inside a product."""

    model = ProductVariant
    extra = 1
    fields = (
        "size",
        "color_name",
        "color_hex",
        "sku",
        "stock",
        "is_active",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configure category management in Django Admin."""

    list_display = (
        "name",
        "slug",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Configure product management in Django Admin."""

    list_display = (
        "name",
        "sku",
        "category",
        "selling_price_display",
        "stock",
        "stock_status",
        "is_featured",
        "is_active",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
        "is_new_arrival",
        "is_best_seller",
        "created_at",
    )

    search_fields = (
        "name",
        "sku",
        "short_description",
        "description",
        "category__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    list_select_related = (
        "category",
    )

    inlines = [
        ProductImageInline,
        ProductVariantInline,
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "sku",
                    "short_description",
                    "description",
                )
            },
        ),
        (
            "Pricing and Inventory",
            {
                "fields": (
                    "price",
                    "discount_price",
                    "stock",
                )
            },
        ),
        (
            "Product Image",
            {
                "fields": (
                    "main_image",
                )
            },
        ),
        (
            "Store Visibility",
            {
                "fields": (
                    "is_active",
                    "is_featured",
                    "is_new_arrival",
                    "is_best_seller",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(
        description="Selling Price",
        ordering="price",
    )
    def selling_price_display(self, obj):
        """Display the current effective product price."""

        return f"Rs. {obj.selling_price:,.2f}"

    @admin.display(
        boolean=True,
        description="In Stock",
    )
    def stock_status(self, obj):
        """Display product stock as an admin boolean icon."""

        return obj.is_in_stock


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Configure standalone product gallery image management."""

    list_display = (
        "product",
        "alt_text",
        "display_order",
    )

    list_filter = (
        "product",
    )

    search_fields = (
        "product__name",
        "alt_text",
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Configure standalone variant management."""

    list_display = (
        "product",
        "size",
        "color_name",
        "sku",
        "stock",
        "is_active",
    )

    list_filter = (
        "is_active",
        "size",
        "color_name",
        "product__category",
    )

    search_fields = (
        "product__name",
        "sku",
        "size",
        "color_name",
    )

    list_select_related = (
        "product",
    )


admin.site.site_header = "ShopSphere Administration"
admin.site.site_title = "ShopSphere Admin"
admin.site.index_title = "Store Management Dashboard"