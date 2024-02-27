from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from profiles.models import UserProfile
from reviews.models import Review, Comment


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
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    user_profiles = UserProfile.objects.filter(user__first_name__icontains=search_query).order_by('user__first_name')

    context = {
        'user_profiles': user_profiles,
        'search_query': search_query,
    }
    return render(request, 'core/user_profiles.html', context)


def profile_detail(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    comment_count = Comment.objects.filter(review__author=user_profile, approved=True).count()
    like_count = Review.objects.filter(author=user_profile).aggregate(total_likes=Count('likes'))['total_likes'] or 0

    context = {
        'user_profile': user_profile,
        'comment_count': comment_count,
        'like_count': like_count,
    }

    return render(request, 'core/profile_detail.html', context)