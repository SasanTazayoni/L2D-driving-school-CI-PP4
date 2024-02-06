from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Review
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
            'Your comment was submitted and is now pending admin approval'
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


@login_required(login_url="login")
def createReview(request):
    profile = UserProfile.objects.get(user=request.user)
    existing_review = Review.objects.filter(author=profile).first()

    if existing_review:
        messages.warning(request, 'You have already made a review.')
        return redirect('reviews')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = profile
            form.save()
            return redirect('reviews')

    context = {'form': form}
    return render(request, "reviews/review_form.html", context)
