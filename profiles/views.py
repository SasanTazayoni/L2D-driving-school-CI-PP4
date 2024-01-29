from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


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


def edit_profile(request):
    """
    Renders the edit profile page and handles form submission
    """

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_page')
    else:
        form = UserProfileForm(instance=profile)

    return render(
        request,
        'profiles/edit_profile.html',
        {'form': form}
    )