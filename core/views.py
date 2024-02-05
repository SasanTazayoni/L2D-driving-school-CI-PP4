from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    """
    Renders the home page
    """
    return render(request, 'core/index.html')


@login_required(login_url='login')
def appointments(request):
    """
    Renders the appointments page if the user is authenticated,
    otherwise redirects to the login page.
    """
    return render(request, 'core/appointments.html')


def contact(request):
    """
    Renders the contact page
    """
    return render(request, 'core/contact.html')


def userProfiles(request):
    return render(request, 'core/user_profiles.html')