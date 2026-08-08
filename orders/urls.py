from django.urls import path

from . import views


app_name = "orders"


urlpatterns = [
    path(
        "",
        views.order_list,
        name="order_list",
    ),
    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),
    path(
        "<str:order_number>/success/",
        views.order_success,
        name="order_success",
    ),
    path(
        "<str:order_number>/cancel/",
        views.cancel_order,
        name="cancel_order",
    ),
    path(
        "<str:order_number>/",
        views.order_detail,
        name="order_detail",
    ),
]
