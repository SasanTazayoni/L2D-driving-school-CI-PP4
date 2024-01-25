from django.shortcuts import render
from .models import UserProfile


def profile_page(request):
    """
    Renders the profile page
    """

    profile = UserProfile.objects.get(user=request.user)

    return render(
        request,
        'user_profile.html',
        {'profile': profile}
    )
