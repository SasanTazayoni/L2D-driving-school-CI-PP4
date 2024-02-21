from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Review, Comment
from .forms import ReviewForm
from .forms import CommentForm
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required


class ReviewList(generic.ListView):
    queryset = Review.objects.filter(approved=True).order_by("-created_on").select_related('author')
    template_name = "reviews/reviews.html"
    paginate_by = 9


def review_detail(request, review_id):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`reviews.Review`.

    **Template:**

    :template:`reviews/review_detail.html`
    """

    queryset = Review.objects.filter(approved=True)
    review = get_object_or_404(Review, id=review_id)
    comments = review.comments.all().order_by("-replied_on")
    comment_count = review.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            profile = UserProfile.objects.get(user=request.user)
            comment.author = profile
            comment.review = review
            comment.save()
            messages.add_message(
            request, messages.SUCCESS,
            'Your comment was submitted and is now pending admin approval.'
        )

    comment_form = CommentForm()

    return render(
        request,
        "reviews/review_detail.html",
        {
            'review': review,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


@login_required(login_url='/accounts/login/')
def edit_comment(request, review_id, comment_id):
    """
    View to edit comments.
    """
    review = get_object_or_404(Review, id=review_id)
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author.user != request.user:
        messages.error(request, 'You are not authorised to edit this comment.')
        return HttpResponseRedirect(reverse('review_detail', args=[review_id]))

    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            edited_comment = comment_form.save(commit=False)
            edited_comment.review = review
            edited_comment.save()
            messages.success(request, 'Comment updated.')
            return HttpResponseRedirect(reverse('review_detail', args=[review_id]))
        else:
            messages.error(request, 'Error updating comment.')
    else:
        comment_form = CommentForm(instance=comment)

    context = {
        'review': review,
        'comment_form': comment_form
    }

    return render(request, 'reviews/review_detail.html', context)


@login_required(login_url='/accounts/login/')
def delete_comment(request, review_id, comment_id):
    """
    View to delete a comment.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    review_id = comment.review.id

    if comment.author.user != request.user:
        messages.error(request, 'You are not authorised to delete this comment.')
        return redirect('review_detail', review_id=review_id)

    if request.method == "POST":
        comment.delete()
        messages.success(request, 'Comment removed.')
        
        source_page = request.POST.get('source_page')
        if source_page == "profile":
            return redirect('profile_page')
        else:
            return redirect(reverse('review_detail', args=[review_id]))


@login_required(login_url='/accounts/login/')
def create_review(request):
    profile = UserProfile.objects.get(user=request.user)
    existing_review = Review.objects.filter(author=profile).first()

    if existing_review:
        messages.info(request, 'You have already made a review.')
        return redirect('profile_page')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = profile
            form.save()
            messages.success(request, 'Your review was submitted and is now pending admin approval.')
            return redirect('profile_page')

    context = {'form': form}
    return render(request, "reviews/review_form.html", context)


@login_required(login_url='/accounts/login/')
def update_review(request, review_id):
    profile = UserProfile.objects.get(user=request.user)
    existing_review = Review.objects.filter(author=profile, id=review_id).first()

    if not existing_review:
        messages.info(request, 'You must create a review before editing.')
        return redirect('profile_page')

    form = ReviewForm(instance=existing_review)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect('profile_page')

    context = {'form': form}
    return render(request, "reviews/review_form.html", context)


@login_required(login_url='/accounts/login/')
def delete_review(request, review_id):
    profile = UserProfile.objects.get(user=request.user)
    existing_review = Review.objects.filter(author=profile, id=review_id).first()

    if not existing_review:
        messages.info(request, 'There is no review to delete.')
        return redirect('profile_page')

    if request.method == 'POST':
        existing_review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('profile_page')
    
    return redirect('profile_page')