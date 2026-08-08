from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import (
    Brand,
    Product,
    ProductAttribute,
    ProductAttributeValue,
)


ATTRIBUTE_DEFINITIONS = [
    {
        "name": "Gender",
        "description": "Who the footwear is designed for.",
        "display_order": 10,
    },
    {
        "name": "Shoe Width",
        "description": "General fit width.",
        "display_order": 20,
    },
    {
        "name": "Material",
        "description": "Primary upper material.",
        "display_order": 30,
    },
    {
        "name": "Sole Material",
        "description": "Primary outsole material.",
        "display_order": 40,
    },
    {
        "name": "Closure Type",
        "description": "How the footwear is secured.",
        "display_order": 50,
    },
    {
        "name": "Heel Type",
        "description": "Heel construction.",
        "display_order": 60,
    },
    {
        "name": "Toe Style",
        "description": "Front shape of the footwear.",
        "display_order": 70,
    },
    {
        "name": "Shoe Style",
        "description": "Overall footwear style.",
        "display_order": 80,
    },
    {
        "name": "Special Feature",
        "description": "Key comfort or performance features.",
        "display_order": 90,
    },
    {
        "name": "Purpose",
        "description": "Recommended activity or use.",
        "display_order": 100,
    },
    {
        "name": "Pattern",
        "description": "Visual pattern or finish.",
        "display_order": 110,
    },
]


PRODUCT_METADATA = {
    "MRP-001": {
        "Gender": ["Unisex"],
        "Shoe Width": ["Standard"],
        "Material": ["Mesh / Synthetic"],
        "Sole Material": ["Rubber"],
        "Closure Type": ["Lace Up"],
        "Heel Type": ["Flat"],
        "Toe Style": ["Round Toe"],
        "Shoe Style": ["Running Shoe"],
        "Special Feature": [
            "Breathable",
            "Cushioned",
        ],
        "Purpose": [
            "Running",
            "Walking",
            "Everyday",
        ],
        "Pattern": ["Color Block"],
    },
    "TFP-002": {
        "Gender": ["Unisex"],
        "Shoe Width": ["Standard"],
        "Material": ["Synthetic / Mesh"],
        "Sole Material": ["Rubber"],
        "Closure Type": ["Lace Up"],
        "Heel Type": ["Flat"],
        "Toe Style": ["Round Toe"],
        "Shoe Style": ["Training Shoe"],
        "Special Feature": [
            "Cushioned",
            "Supportive",
            "Traction",
        ],
        "Purpose": [
            "Training",
            "Outdoor Walking",
            "Everyday",
        ],
        "Pattern": ["Color Block"],
    },
    "UEP-003": {
        "Gender": ["Unisex"],
        "Shoe Width": ["Standard"],
        "Material": ["Synthetic Leather"],
        "Sole Material": ["Rubber"],
        "Closure Type": ["Lace Up"],
        "Heel Type": ["Flat"],
        "Toe Style": ["Round Toe"],
        "Shoe Style": ["High-Top Sneaker"],
        "Special Feature": [
            "Padded Ankle",
            "Flexible Sole",
        ],
        "Purpose": [
            "Lifestyle",
            "Travel",
            "Everyday",
        ],
        "Pattern": ["Solid"],
    },
}


class Command(BaseCommand):
    help = (
        "Create ShopSphere brand and standard filterable "
        "product attributes for the current catalogue."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        brand, _ = Brand.objects.get_or_create(
            name="ShopSphere",
            defaults={
                "description": (
                    "ShopSphere footwear and movement collection."
                ),
                "is_active": True,
            },
        )

        attributes = {}

        for definition in ATTRIBUTE_DEFINITIONS:
            attribute, _ = ProductAttribute.objects.update_or_create(
                name=definition["name"],
                defaults={
                    "description": definition["description"],
                    "is_filterable": True,
                    "is_visible": True,
                    "is_active": True,
                    "display_order": definition["display_order"],
                },
            )

            attributes[attribute.name] = attribute

        seeded_products = 0
        seeded_values = 0

        for sku, metadata in PRODUCT_METADATA.items():
            product = Product.objects.filter(
                sku=sku
            ).first()

            if not product:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped missing product {sku}."
                    )
                )
                continue

            if product.brand_id != brand.id:
                product.brand = brand
                product.save(
                    update_fields=[
                        "brand",
                        "updated_at",
                    ]
                )

            seeded_products += 1

            for attribute_name, values in metadata.items():
                attribute = attributes[attribute_name]

                for display_order, value in enumerate(
                    values,
                    start=1,
                ):
                    _, created = ProductAttributeValue.objects.get_or_create(
                        product=product,
                        attribute=attribute,
                        value=value,
                        defaults={
                            "display_order": display_order,
                        },
                    )

                    if created:
                        seeded_values += 1

        self.stdout.write(
            self.style.SUCCESS(
                (
                    f"ShopSphere catalogue metadata ready: "
                    f"{seeded_products} product(s), "
                    f"{len(attributes)} attributes, "
                    f"{seeded_values} new value(s)."
                )
            )
        )
