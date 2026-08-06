from django.contrib import admin

from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    """Manage customer profiles through Django Admin."""

    list_display = (
        "user",
        "phone",
        "city",
        "province",
        "country",
        "updated_at",
    )

    list_filter = (
        "country",
        "province",
        "city",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "phone",
        "city",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "user",
    )