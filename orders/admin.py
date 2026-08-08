from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = (
        "product_name",
        "product_sku",
        "variant_sku",
        "size",
        "color_name",
        "unit_price",
        "quantity",
        "line_total",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "recipient_name",
        "total",
        "payment_status",
        "fulfillment_status",
        "created_at",
    )

    list_filter = (
        "payment_method",
        "payment_status",
        "fulfillment_status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "recipient_name",
        "phone",
        "email",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "order_number",
        "user",
        "recipient_name",
        "phone",
        "email",
        "address_line_1",
        "address_line_2",
        "city",
        "province",
        "postal_code",
        "landmark",
        "customer_note",
        "subtotal",
        "shipping_amount",
        "total",
        "payment_method",
        "created_at",
        "updated_at",
    )

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product_name",
        "variant_sku",
        "size",
        "color_name",
        "quantity",
        "line_total",
    )

    search_fields = (
        "order__order_number",
        "product_name",
        "product_sku",
        "variant_sku",
    )
