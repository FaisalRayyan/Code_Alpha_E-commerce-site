from django.contrib import admin

from .models import (
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductImage,
    ProductVariant,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = (
        "image",
        "alt_text",
        "display_order",
    )


class ProductVariantInline(admin.TabularInline):
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


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    autocomplete_fields = (
        "attribute",
    )
    fields = (
        "attribute",
        "value",
        "display_order",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
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


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
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

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_filterable",
        "is_visible",
        "is_active",
        "display_order",
    )

    list_filter = (
        "is_filterable",
        "is_visible",
        "is_active",
    )

    list_editable = (
        "is_filterable",
        "is_visible",
        "is_active",
        "display_order",
    )

    search_fields = (
        "name",
        "slug",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "brand",
        "category",
        "selling_price_display",
        "stock",
        "stock_status",
        "is_featured",
        "is_active",
    )

    list_filter = (
        "brand",
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
        "brand__name",
        "short_description",
        "description",
        "category__name",
        "attribute_values__value",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    list_select_related = (
        "brand",
        "category",
    )

    inlines = [
        ProductImageInline,
        ProductVariantInline,
        ProductAttributeValueInline,
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "brand",
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
        return f"Rs. {obj.selling_price:,.2f}"

    @admin.display(
        boolean=True,
        description="In Stock",
    )
    def stock_status(self, obj):
        return obj.is_in_stock


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
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
        "product__brand",
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


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "attribute",
        "value",
        "display_order",
    )

    list_filter = (
        "attribute",
        "product__brand",
        "product__category",
    )

    search_fields = (
        "product__name",
        "product__sku",
        "attribute__name",
        "value",
    )

    autocomplete_fields = (
        "product",
        "attribute",
    )

    list_select_related = (
        "product",
        "attribute",
    )


admin.site.site_header = "ShopSphere Administration"
admin.site.site_title = "ShopSphere Admin"
admin.site.index_title = "Store Management Dashboard"
