from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


def userLogin(request):

    if request.user.is_authenticated:
        return redirect('profile_page')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            return render(request, 'profiles/login_register.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('reviews')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'profiles/login_register.html')


@login_required
def userLogout(request):
    logout(request)
    messages.error(request, 'You have logged out')
    return redirect('login')


@login_required(login_url="login")
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


@login_required(login_url="login")
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