from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import (
    Category,
    Product,
    ProductVariant,
)


PRODUCTS = [
    {
        "category": "Running",
        "name": "Motion Runner Pro",
        "sku": "MRP-001",
        "short_description": (
            "A lightweight everyday runner with breathable support "
            "and responsive cushioning."
        ),
        "description": (
            "Motion Runner Pro is designed for daily movement, "
            "light runs, commuting, and long walking sessions. "
            "Its breathable upper helps manage heat, while the "
            "cushioned midsole softens repeated impact. The stable "
            "rubber outsole gives controlled grip on common urban "
            "surfaces."
        ),
        "price": "18499.00",
        "discount_price": "15999.00",
        "stock": 24,
        "image": "motion-runner-pro.webp",
        "is_featured": True,
        "is_new_arrival": True,
        "is_best_seller": False,
        "color_name": "Navy / Stone",
        "color_hex": "#26364F",
        "variant_prefix": "MRP-NVY",
    },
    {
        "category": "Training",
        "name": "Terrain Flow Pro",
        "sku": "TFP-002",
        "short_description": (
            "A cushioned performance trainer with a stable base "
            "and road-to-trail traction."
        ),
        "description": (
            "Terrain Flow Pro combines a supportive heel structure, "
            "flexible forefoot movement, and a traction-focused outsole. "
            "It is suited to training, outdoor walking, and active "
            "daily wear where extra stability and surface control "
            "are important."
        ),
        "price": "19999.00",
        "discount_price": "17499.00",
        "stock": 18,
        "image": "terrain-flow-pro.webp",
        "is_featured": True,
        "is_new_arrival": False,
        "is_best_seller": True,
        "color_name": "Silver / Blue",
        "color_hex": "#B8C1CF",
        "variant_prefix": "TFP-SLV",
    },
    {
        "category": "Lifestyle",
        "name": "Urban Elevate Pro",
        "sku": "UEP-003",
        "short_description": (
            "A high-top lifestyle shoe made for everyday comfort, "
            "support, and clean street styling."
        ),
        "description": (
            "Urban Elevate Pro brings padded ankle support and a "
            "durable upper into an everyday silhouette. The soft "
            "inner lining supports long wear, while the flexible "
            "sole keeps the shoe practical for work, travel, and "
            "casual city movement."
        ),
        "price": "16999.00",
        "discount_price": "14999.00",
        "stock": 20,
        "image": "urban-elevate-pro.webp",
        "is_featured": True,
        "is_new_arrival": True,
        "is_best_seller": False,
        "color_name": "Tan / Black",
        "color_hex": "#B77A42",
        "variant_prefix": "UEP-TAN",
    },
]


class Command(BaseCommand):
    help = (
        "Create the three ShopSphere starter products "
        "with their variants."
    )

    @transaction.atomic
    def handle(self, *args, **options):

        image_directory = (
            Path(settings.BASE_DIR)
            / "static"
            / "images"
            / "products"
            / "real"
        )

        missing_images = [
            product["image"]
            for product in PRODUCTS
            if not (
                image_directory
                / product["image"]
            ).exists()
        ]

        if missing_images:
            self.stderr.write(
                self.style.ERROR(
                    "Missing image files: "
                    + ", ".join(missing_images)
                )
            )

            return

        for product_data in PRODUCTS:

            category, _ = (
                Category.objects.get_or_create(
                    name=product_data["category"],
                    defaults={
                        "description": (
                            f"{product_data['category']} "
                            "footwear collection."
                        ),
                        "is_active": True,
                    },
                )
            )

            product, created = (
                Product.objects.update_or_create(
                    sku=product_data["sku"],
                    defaults={
                        "category": category,
                        "name": product_data["name"],
                        "short_description": (
                            product_data[
                                "short_description"
                            ]
                        ),
                        "description": (
                            product_data[
                                "description"
                            ]
                        ),
                        "price": (
                            product_data[
                                "price"
                            ]
                        ),
                        "discount_price": (
                            product_data[
                                "discount_price"
                            ]
                        ),
                        "stock": (
                            product_data[
                                "stock"
                            ]
                        ),
                        "is_active": True,
                        "is_featured": (
                            product_data[
                                "is_featured"
                            ]
                        ),
                        "is_new_arrival": (
                            product_data[
                                "is_new_arrival"
                            ]
                        ),
                        "is_best_seller": (
                            product_data[
                                "is_best_seller"
                            ]
                        ),
                    },
                )
            )

            image_path = (
                image_directory
                / product_data["image"]
            )

            with image_path.open("rb") as image_file:

                product.main_image.save(
                    product_data["image"],
                    File(image_file),
                    save=False,
                )

            product.save()

            for size in (
                "40",
                "41",
                "42",
            ):

                ProductVariant.objects.update_or_create(
                    product=product,
                    size=size,
                    color_name=(
                        product_data[
                            "color_name"
                        ]
                    ),
                    defaults={
                        "color_hex": (
                            product_data[
                                "color_hex"
                            ]
                        ),
                        "sku": (
                            f"{product_data['variant_prefix']}"
                            f"-{size}"
                        ),
                        "stock": max(
                            product_data[
                                "stock"
                            ] // 3,
                            1,
                        ),
                        "is_active": True,
                    },
                )

            status = (
                "Created"
                if created
                else "Updated"
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"{status}: {product.name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "ShopSphere starter catalogue "
                "is ready."
            )
        )