from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from reviews.models import Comment
from .models import UserProfile
from .forms import UserProfileForm


@login_required(login_url="login")
def profile_page(request):
    """
    Renders the profile page
    """

    profile = get_object_or_404(UserProfile, user=request.user)
    try:
        review_id = profile.review.id
    except ObjectDoesNotExist:
        review_id = None

    comments = Comment.objects.filter(author=profile)

    context = {
        'profile': profile,
        'review_id': review_id,
        'comments': comments
    }

    return render(
        request,
        'profiles/profile.html',
        context
    )


@login_required(login_url="login")
def edit_profile(request):
    """
    Renders the edit profile page and handles form submission
    """

    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, username=request.user)

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES,
            instance=profile,
            initial={
                'username': user.username, 'email': user.email
            }
        )
        if form.is_valid():
            user.email = request.POST.get('email')
            user.save()
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_page')

    else:
        form = UserProfileForm(
            instance=profile,
            initial={
                'username': user.username, 'email': user.email
            }
        )

    template = 'profiles/edit_profile.html',
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required(login_url="login")
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted')
        return redirect('home')
    else:
        return redirect('profile_page')
