from django.shortcuts import render, get_object_or_404
from .models import UserProfile


def profile_page(request):
    """
    Renders the profile page
    """

    profile = get_object_or_404(UserProfile, user=request.user)

    return render(
        request,
        'profiles/user_profile.html',
        {'profile': profile}
    )
