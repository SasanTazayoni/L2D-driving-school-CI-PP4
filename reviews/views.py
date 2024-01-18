from django.shortcuts import render
from django.views import generic
from .models import Review

# Create your views here.
class ReviewList(generic.ListView):
    queryset = Review.objects.filter(status=1).order_by("-created_on")
    template_name = "reviews/reviews.html"
    paginate_by = 10