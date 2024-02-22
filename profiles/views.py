from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from reviews.models import Review, Comment
from .models import UserProfile
from .forms import UserProfileForm


@login_required(login_url='/accounts/login/')
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
    comment_count = comments.count()
    like_count = Review.objects.filter(id=review_id).first().likes.count()

    context = {
        'profile': profile,
        'review_id': review_id,
        'comments': comments,
        'comment_count': comment_count,
        'like_count': like_count,
    }

    return render(
        request,
        'profiles/profile.html',
        context
    )


@login_required(login_url='/accounts/login/')
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
                'email': user.email, 'first_name': user.first_name
            }
        )
        if form.is_valid():
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.save()
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_page')

    else:
        form = UserProfileForm(
            instance=profile,
            initial={
                'email': user.email, 'first_name': user.first_name
            }
        )

    template = 'profiles/edit_profile.html',
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required(login_url='/accounts/login/')
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    else:
        return redirect('profile_page')
