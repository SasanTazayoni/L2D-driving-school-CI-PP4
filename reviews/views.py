from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Review
from .forms import CommentForm

# Create your views here.
class ReviewList(generic.ListView):
    queryset = Review.objects.filter(approved=True).order_by("-created_on")
    template_name = "reviews/reviews.html"
    paginate_by = 10


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
            comment.author = request.user
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