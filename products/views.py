from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.db.models import (
    Case,
    Count,
    DecimalField,
    Exists,
    F,
    OuterRef,
    Prefetch,
    Q,
    When,
)
from django.shortcuts import get_object_or_404, render

from .models import (
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductVariant,
)


def product_list(request):
    """Display the ShopSphere catalogue with scalable marketplace facets."""

    active_variants = ProductVariant.objects.filter(
        is_active=True
    ).order_by(
        "size",
        "color_name",
    )

    products = (
        Product.objects
        .filter(is_active=True)
        .select_related(
            "brand",
            "category",
        )
        .prefetch_related(
            Prefetch(
                "variants",
                queryset=active_variants,
                to_attr="active_variants",
            )
        )
        .annotate(
            effective_price=Case(
                When(
                    discount_price__isnull=False,
                    then=F("discount_price"),
                ),
                default=F("price"),
                output_field=DecimalField(
                    max_digits=10,
                    decimal_places=2,
                ),
            ),
            has_variant_stock=Exists(
                ProductVariant.objects.filter(
                    product=OuterRef("pk"),
                    is_active=True,
                    stock__gt=0,
                )
            ),
        )
    )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    query = request.GET.get("q", "").strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(sku__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(brand__name__icontains=query)
            | Q(variants__color_name__icontains=query)
            | Q(variants__size__icontains=query)
            | Q(attribute_values__value__icontains=query)
            | Q(attribute_values__attribute__name__icontains=query)
        )

    # ---------------------------------------------------------
    # Category
    # ---------------------------------------------------------

    category_slug = request.GET.get(
        "category",
        "",
    ).strip()

    if category_slug:
        products = products.filter(
            category__slug=category_slug,
            category__is_active=True,
        )

    # ---------------------------------------------------------
    # Brand — multi-select
    # ---------------------------------------------------------

    selected_brands = [
        value.strip()
        for value in request.GET.getlist("brand")
        if value.strip()
    ]

    if selected_brands:
        products = products.filter(
            brand__slug__in=selected_brands,
            brand__is_active=True,
        )

    # ---------------------------------------------------------
    # Price
    # ---------------------------------------------------------

    price_min = request.GET.get(
        "price_min",
        "",
    ).strip()

    price_max = request.GET.get(
        "price_max",
        "",
    ).strip()

    if price_min:
        try:
            price_min_value = Decimal(price_min)

            if price_min_value < 0:
                raise InvalidOperation

            products = products.filter(
                effective_price__gte=price_min_value
            )
        except (InvalidOperation, TypeError, ValueError):
            price_min = ""

    if price_max:
        try:
            price_max_value = Decimal(price_max)

            if price_max_value < 0:
                raise InvalidOperation

            products = products.filter(
                effective_price__lte=price_max_value
            )
        except (InvalidOperation, TypeError, ValueError):
            price_max = ""

    # ---------------------------------------------------------
    # Size / color
    # ---------------------------------------------------------

    selected_sizes = [
        value.strip()
        for value in request.GET.getlist("size")
        if value.strip()
    ]

    selected_colors = [
        value.strip()
        for value in request.GET.getlist("color")
        if value.strip()
    ]

    if selected_sizes:
        products = products.filter(
            variants__is_active=True,
            variants__size__in=selected_sizes,
        )

    if selected_colors:
        products = products.filter(
            variants__is_active=True,
            variants__color_name__in=selected_colors,
        )

    # ---------------------------------------------------------
    # Dynamic product attributes
    # ---------------------------------------------------------

    filter_attributes = list(
        ProductAttribute.objects
        .filter(
            is_active=True,
            is_filterable=True,
        )
        .order_by(
            "display_order",
            "name",
        )
    )

    selected_attributes = {}

    for attribute in filter_attributes:
        parameter_name = f"attr_{attribute.slug}"

        values = [
            value.strip()
            for value in request.GET.getlist(parameter_name)
            if value.strip()
        ]

        if not values:
            continue

        selected_attributes[attribute.slug] = values

        # A single facet uses OR between selected values.
        # Separate facets are applied in separate filter calls,
        # therefore they combine as AND across different attributes.
        products = products.filter(
            attribute_values__attribute=attribute,
            attribute_values__value__in=values,
        )

    # ---------------------------------------------------------
    # Availability / merchandising flags
    # ---------------------------------------------------------

    in_stock_only = (
        request.GET.get("in_stock") == "1"
    )

    new_only = (
        request.GET.get("new") == "1"
    )

    best_only = (
        request.GET.get("best") == "1"
    )

    if in_stock_only:
        products = products.filter(
            Q(stock__gt=0)
            | Q(
                variants__is_active=True,
                variants__stock__gt=0,
            )
        )

    if new_only:
        products = products.filter(
            is_new_arrival=True
        )

    if best_only:
        products = products.filter(
            is_best_seller=True
        )

    products = products.distinct()

    # ---------------------------------------------------------
    # Sorting
    # ---------------------------------------------------------

    sort = request.GET.get(
        "sort",
        "featured",
    ).strip()

    sort_options = {
        "featured": (
            "-is_featured",
            "-is_best_seller",
            "-is_new_arrival",
            "-created_at",
        ),
        "newest": (
            "-created_at",
        ),
        "best_selling": (
            "-is_best_seller",
            "-is_featured",
            "-created_at",
        ),
        "price_asc": (
            "effective_price",
            "name",
        ),
        "price_desc": (
            "-effective_price",
            "name",
        ),
        "name_asc": (
            "name",
        ),
    }

    if sort not in sort_options:
        sort = "featured"

    products = products.order_by(
        *sort_options[sort]
    )

    # ---------------------------------------------------------
    # Sidebar base data
    # ---------------------------------------------------------

    categories = (
        Category.objects
        .filter(is_active=True)
        .annotate(
            active_product_count=Count(
                "products",
                filter=Q(
                    products__is_active=True
                ),
                distinct=True,
            )
        )
        .filter(active_product_count__gt=0)
        .order_by("name")
    )

    brands = (
        Brand.objects
        .filter(is_active=True)
        .annotate(
            active_product_count=Count(
                "products",
                filter=Q(
                    products__is_active=True
                ),
                distinct=True,
            )
        )
        .filter(active_product_count__gt=0)
        .order_by("name")
    )

    variant_source = (
        ProductVariant.objects
        .filter(
            is_active=True,
            product__is_active=True,
        )
    )

    sizes = list(
        variant_source
        .exclude(size="")
        .values_list(
            "size",
            flat=True,
        )
        .distinct()
        .order_by("size")
    )

    colors = list(
        variant_source
        .exclude(color_name="")
        .values(
            "color_name",
            "color_hex",
        )
        .distinct()
        .order_by("color_name")
    )

    # Build reusable dynamic facet groups with product counts.
    attribute_rows = (
        ProductAttributeValue.objects
        .filter(
            attribute__in=filter_attributes,
            product__is_active=True,
        )
        .values(
            "attribute_id",
            "value",
        )
        .annotate(
            product_count=Count(
                "product",
                distinct=True,
            )
        )
        .order_by(
            "attribute_id",
            "value",
        )
    )

    values_by_attribute = {}

    for row in attribute_rows:
        values_by_attribute.setdefault(
            row["attribute_id"],
            [],
        ).append(row)

    attribute_filters = []

    for attribute in filter_attributes:
        choices = []

        for row in values_by_attribute.get(
            attribute.id,
            [],
        ):
            choices.append(
                {
                    "value": row["value"],
                    "count": row["product_count"],
                    "is_selected": (
                        row["value"]
                        in selected_attributes.get(
                            attribute.slug,
                            [],
                        )
                    ),
                }
            )

        if not choices:
            continue

        attribute_filters.append(
            {
                "name": attribute.name,
                "slug": attribute.slug,
                "description": attribute.description,
                "choices": choices,
            }
        )

    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------

    paginator = Paginator(
        products,
        24,
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    query_params = request.GET.copy()
    query_params.pop("page", None)

    # Used by sort form and active-filter rendering.
    selected_attribute_query_items = []

    for attribute_slug, values in selected_attributes.items():
        for value in values:
            selected_attribute_query_items.append(
                (
                    f"attr_{attribute_slug}",
                    value,
                )
            )

    active_attribute_chips = []

    attribute_name_map = {
        attribute.slug: attribute.name
        for attribute in filter_attributes
    }

    for attribute_slug, values in selected_attributes.items():
        for value in values:
            active_attribute_chips.append(
                {
                    "name": attribute_name_map.get(
                        attribute_slug,
                        attribute_slug.replace("-", " ").title(),
                    ),
                    "value": value,
                }
            )

    context = {
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "paginator": paginator,
        "result_count": paginator.count,

        "categories": categories,
        "brands": brands,
        "sizes": sizes,
        "colors": colors,
        "attribute_filters": attribute_filters,

        "query": query,
        "selected_category": category_slug,
        "selected_brands": selected_brands,
        "selected_sizes": selected_sizes,
        "selected_colors": selected_colors,
        "selected_attribute_query_items": selected_attribute_query_items,
        "active_attribute_chips": active_attribute_chips,

        "price_min": price_min,
        "price_max": price_max,

        "in_stock_only": in_stock_only,
        "new_only": new_only,
        "best_only": best_only,

        "sort": sort,
        "filter_query": query_params.urlencode(),
    }

    return render(
        request,
        "products/product_list.html",
        context,
    )


def product_detail(request, slug):
    """Display one ShopSphere product with live variant information."""

    product = get_object_or_404(
        Product.objects
        .select_related("brand", "category")
        .prefetch_related(
            "images",
            "variants",
            "attribute_values__attribute",
        ),
        slug=slug,
        is_active=True,
    )

    active_variants = list(
        product.variants
        .filter(is_active=True)
        .order_by(
            "color_name",
            "size",
        )
    )

    variant_data = [
        {
            "id": variant.id,
            "size": variant.size,
            "color_name": variant.color_name,
            "color_hex": variant.color_hex or "#303744",
            "stock": variant.stock,
            "sku": variant.sku,
        }
        for variant in active_variants
    ]

    colors_by_name = {}

    for variant in active_variants:
        if variant.color_name not in colors_by_name:
            colors_by_name[variant.color_name] = {
                "name": variant.color_name,
                "hex": variant.color_hex or "#303744",
                "has_stock": False,
            }

        if variant.stock > 0:
            colors_by_name[variant.color_name][
                "has_stock"
            ] = True

    def size_sort_key(value):
        try:
            return (
                0,
                float(value),
            )
        except (TypeError, ValueError):
            return (
                1,
                str(value).lower(),
            )

    sizes = sorted(
        {
            variant.size
            for variant in active_variants
            if variant.size
        },
        key=size_sort_key,
    )

    total_variant_stock = sum(
        variant.stock
        for variant in active_variants
    )

    if active_variants:
        available_stock = total_variant_stock
        has_stock = total_variant_stock > 0
    else:
        available_stock = product.stock
        has_stock = product.stock > 0

    discount_percent = None

    if (
        product.discount_price is not None
        and product.price
        and product.price > 0
    ):
        discount_percent = int(
            round(
                (
                    (
                        product.price
                        - product.discount_price
                    )
                    / product.price
                )
                * 100
            )
        )

    visible_attribute_values = (
        product.attribute_values
        .filter(
            attribute__is_active=True,
            attribute__is_visible=True,
        )
        .select_related("attribute")
        .order_by(
            "attribute__display_order",
            "attribute__name",
            "display_order",
            "value",
        )
    )

    visible_attribute_map = {}

    for attribute_value in visible_attribute_values:
        entry = visible_attribute_map.setdefault(
            attribute_value.attribute_id,
            {
                "name": attribute_value.attribute.name,
                "values": [],
            },
        )

        entry["values"].append(
            attribute_value.value
        )

    visible_attributes = list(
        visible_attribute_map.values()
    )

    related_products = (
        Product.objects
        .filter(
            category=product.category,
            is_active=True,
        )
        .exclude(id=product.id)
        .select_related("brand", "category")
        .prefetch_related("variants")
        .order_by(
            "-is_best_seller",
            "-is_new_arrival",
            "-created_at",
        )[:4]
    )

    context = {
        "product": product,
        "active_variants": active_variants,
        "variant_data": variant_data,
        "product_colors": list(
            colors_by_name.values()
        ),
        "product_sizes": sizes,
        "available_stock": available_stock,
        "has_stock": has_stock,
        "discount_percent": discount_percent,
        "visible_attributes": visible_attributes,
        "related_products": related_products,
    }

    return render(
        request,
        "products/product_detail.html",
        context,
    )
