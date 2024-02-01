from django.shortcuts import render


def home(request):
    """
    Renders the home page
    """
    return render(request, 'core/index.html')


def appointments(request):
    """
    Renders the appointments page
    """
    return render(request, 'core/appointments.html')


def contact(request):
    """
    Renders the contact page
    """
    return render(request, 'core/contact.html')