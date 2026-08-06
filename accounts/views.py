from django.contrib import messages
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from cart.services import merge_guest_cart_into_user

from .forms import (
    CustomerProfileUpdateForm,
    CustomerRegistrationForm,
    CustomerUserUpdateForm,
)
from .models import CustomerProfile


def register(request):
    """Create a new ShopSphere customer account."""

    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                (
                    f"Welcome, {user.first_name}. "
                    "Your ShopSphere account has been created."
                ),
            )

            return redirect("accounts:login")
    else:
        form = CustomerRegistrationForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/register.html",
        context,
    )


def login_view(request):
    """Authenticate a customer and merge their guest cart."""

    if request.user.is_authenticated:
        return redirect("core:home")

    guest_session_key = request.session.session_key

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            user = form.get_user()

            auth_login(
                request,
                user,
            )

            merge_guest_cart_into_user(
                guest_session_key,
                user,
            )

            customer_name = user.first_name or user.username

            messages.success(
                request,
                f"Welcome back, {customer_name}.",
            )

            return redirect("core:home")
    else:
        form = AuthenticationForm(request)

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/login.html",
        context,
    )


@require_POST
def logout_view(request):
    """Log out the current ShopSphere customer."""

    auth_logout(request)

    messages.success(
        request,
        "You have been logged out successfully.",
    )

    return redirect("core:home")


@login_required
def profile(request):
    """Display the authenticated customer's account profile."""

    customer_profile, _ = CustomerProfile.objects.get_or_create(
        user=request.user,
    )

    context = {
        "customer_profile": customer_profile,
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )


@login_required
@transaction.atomic
def edit_profile(request):
    """Update customer account and shipping information."""

    customer_profile, _ = CustomerProfile.objects.get_or_create(
        user=request.user,
    )

    if request.method == "POST":
        user_form = CustomerUserUpdateForm(
            request.POST,
            instance=request.user,
        )

        profile_form = CustomerProfileUpdateForm(
            request.POST,
            instance=customer_profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Your ShopSphere profile has been updated.",
            )

            return redirect("accounts:profile")
    else:
        user_form = CustomerUserUpdateForm(
            instance=request.user,
        )

        profile_form = CustomerProfileUpdateForm(
            instance=customer_profile,
        )

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(
        request,
        "accounts/edit_profile.html",
        context,
    )
@login_required
def change_password(request):
    """Allow the authenticated customer to change their password."""

    if request.method == "POST":
        form = PasswordChangeForm(
            user=request.user,
            data=request.POST,
        )

        if form.is_valid():
            updated_user = form.save()

            update_session_auth_hash(
                request,
                updated_user,
            )

            messages.success(
                request,
                "Your password has been changed successfully.",
            )

            return redirect("accounts:profile")
    else:
        form = PasswordChangeForm(
            user=request.user,
        )

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/change_password.html",
        context,
    )