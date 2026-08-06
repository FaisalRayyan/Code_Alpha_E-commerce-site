from django.conf import settings
from django.db import models


class CustomerProfile(models.Model):
    """Store additional information for a ShopSphere customer."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    address_line_1 = models.CharField(
        max_length=180,
        blank=True,
    )

    address_line_2 = models.CharField(
        max_length=180,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    province = models.CharField(
        max_length=100,
        blank=True,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="Pakistan",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.user.username}'s profile"