from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Review

# Create your views here.
class ReviewList(generic.ListView):
    queryset = Review.objects.filter(status=1).order_by("-created_on")
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

    queryset = Review.objects.filter(status=1)
    review = get_object_or_404(Review, id=review_id)
    comments = review.comments.all().order_by("-replied_on")
    comment_count = review.comments.filter(approved=True).count()

    return render(
        request,
        "reviews/review_detail.html",
        {
            'review': review,
            "comments": comments,
            "comment_count": comment_count,
        },
    )