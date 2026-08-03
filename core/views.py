from django.shortcuts import render


def home(request):
    """Display the ShopSphere home page."""
    return render(request, "core/home.html")