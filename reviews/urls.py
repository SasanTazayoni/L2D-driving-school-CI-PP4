from . import views
from django.urls import path

urlpatterns = [
    path("", views.ReviewList.as_view(), name="reviews"),
    path("<str:review_id>/", views.review_detail, name="review_detail"),
    path("create-review/", views.create_review, name="create-review"),
]