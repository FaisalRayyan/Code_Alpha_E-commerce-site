from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import CustomerProfile


User = get_user_model()


class CustomerRegistrationForm(UserCreationForm):
    """Register a new ShopSphere customer."""

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="First name",
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Last name",
    )

    email = forms.EmailField(
        required=True,
        label="Email address",
    )

    phone = forms.CharField(
        max_length=16,
        required=True,
        label="Phone number",
        help_text="Use 10–15 digits, optionally starting with +.",
    )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "password1",
            "password2",
        )

    def clean_email(self):
        """Prevent duplicate customer email addresses."""

        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_phone(self):
        """Validate and normalize the customer phone number."""

        phone = self.cleaned_data["phone"].strip()

        normalized_phone = (
            phone
            .replace(" ", "")
            .replace("-", "")
        )

        digits = (
            normalized_phone[1:]
            if normalized_phone.startswith("+")
            else normalized_phone
        )

        if not digits.isdigit() or not 10 <= len(digits) <= 15:
            raise forms.ValidationError(
                "Enter a valid phone number containing 10–15 digits."
            )

        return normalized_phone

    @transaction.atomic
    def save(self, commit=True):
        """Create user and update the related customer profile."""

        user = super().save(commit=False)

        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            profile, _ = CustomerProfile.objects.get_or_create(
                user=user,
            )

            profile.phone = self.cleaned_data["phone"]
            profile.save()

        return user


class CustomerUserUpdateForm(forms.ModelForm):
    """Update the customer's core Django user information."""

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
        )

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "First name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Last name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email address",
                }
            ),
        }

    def clean_email(self):
        """Prevent use of another customer's email address."""

        email = self.cleaned_data["email"].strip().lower()

        email_exists = (
            User.objects
            .filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
        )

        if email_exists:
            raise forms.ValidationError(
                "Another account is already using this email."
            )

        return email


class CustomerProfileUpdateForm(forms.ModelForm):
    """Update customer contact and delivery information."""

    class Meta:
        model = CustomerProfile

        fields = (
            "phone",
            "address_line_1",
            "address_line_2",
            "city",
            "province",
            "postal_code",
            "country",
        )

        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "03001234567",
                }
            ),
            "address_line_1": forms.TextInput(
                attrs={
                    "placeholder": "House, street or building",
                }
            ),
            "address_line_2": forms.TextInput(
                attrs={
                    "placeholder": "Area or additional details",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "placeholder": "City",
                }
            ),
            "province": forms.TextInput(
                attrs={
                    "placeholder": "Province",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "placeholder": "Postal code",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "placeholder": "Country",
                }
            ),
        }

    def clean_phone(self):
        """Validate and normalize the customer phone number."""

        phone = self.cleaned_data["phone"].strip()

        if not phone:
            return ""

        normalized_phone = (
            phone
            .replace(" ", "")
            .replace("-", "")
        )

        digits = (
            normalized_phone[1:]
            if normalized_phone.startswith("+")
            else normalized_phone
        )

        if not digits.isdigit() or not 10 <= len(digits) <= 15:
            raise forms.ValidationError(
                "Enter a valid phone number containing 10–15 digits."
            )

        return normalized_phone