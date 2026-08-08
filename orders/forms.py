from django import forms
from django.core.validators import RegexValidator

from .models import Order


PAKISTAN_PROVINCES = [
    ("", "Select province / region"),
    ("Punjab", "Punjab"),
    ("Sindh", "Sindh"),
    ("Khyber Pakhtunkhwa", "Khyber Pakhtunkhwa"),
    ("Balochistan", "Balochistan"),
    ("Islamabad Capital Territory", "Islamabad Capital Territory"),
    ("Gilgit-Baltistan", "Gilgit-Baltistan"),
    ("Azad Jammu & Kashmir", "Azad Jammu & Kashmir"),
]


phone_validator = RegexValidator(
    regex=r"^\+?[0-9][0-9\s\-]{8,19}$",
    message=(
        "Enter a valid phone number using digits, "
        "spaces or hyphens."
    ),
)


class CheckoutForm(forms.Form):
    """Collect the delivery snapshot used for one order."""

    recipient_name = forms.CharField(
        max_length=160,
        label="Full name",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "name",
                "placeholder": "Recipient full name",
            }
        ),
    )

    phone = forms.CharField(
        max_length=30,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                "autocomplete": "tel",
                "placeholder": "+92 3XX XXXXXXX",
            }
        ),
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Email address (optional)",
            }
        ),
    )

    address_line_1 = forms.CharField(
        max_length=220,
        label="Address",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "address-line1",
                "placeholder": "House / building / street",
            }
        ),
    )

    address_line_2 = forms.CharField(
        max_length=220,
        required=False,
        label="Address line 2",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "address-line2",
                "placeholder": "Apartment, floor, area (optional)",
            }
        ),
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "address-level2",
                "placeholder": "City",
            }
        ),
    )

    province = forms.ChoiceField(
        choices=PAKISTAN_PROVINCES,
        widget=forms.Select(
            attrs={
                "autocomplete": "address-level1",
            }
        ),
    )

    postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "postal-code",
                "placeholder": "Postal code (optional)",
            }
        ),
    )

    landmark = forms.CharField(
        max_length=160,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nearby landmark (optional)",
            }
        ),
    )

    customer_note = forms.CharField(
        required=False,
        label="Delivery note",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": (
                    "Optional instructions for this order"
                ),
            }
        ),
    )

    payment_method = forms.ChoiceField(
        choices=Order.PaymentMethod.choices,
        initial=Order.PaymentMethod.CASH_ON_DELIVERY,
        widget=forms.RadioSelect,
    )
