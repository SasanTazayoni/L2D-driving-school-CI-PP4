from . import views
from django.urls import path

urlpatterns = [
    path("", views.ReviewList.as_view(), name="reviews"),
    path("<int:review_id>/", views.review_detail, name="review_detail"),
    path("create-review/", views.create_review, name="create_review"),
    path('update-review/<int:review_id>/', views.update_review, name='update_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('edit-comment/<int:review_id>/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]