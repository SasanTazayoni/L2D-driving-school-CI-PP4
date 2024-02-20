from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile


def home(request):
    """
    Renders the home page
    """
    return render(request, 'core/index.html')


@login_required(login_url='/accounts/login/')
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


def user_profiles(request):
    """
    Renders the user profiles page
    """
    user_profiles = UserProfile.objects.all()
    context = {'user_profiles': user_profiles}
    return render(request, 'core/user_profiles.html', context)


def profile_detail(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    context = {'user_profile': user_profile}
    return render(request, 'core/profile_detail.html', context)