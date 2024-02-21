from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_profiles, name="user_profiles"),
    path("<int:user_id>/", views.profile_detail, name="profile_detail"),
]