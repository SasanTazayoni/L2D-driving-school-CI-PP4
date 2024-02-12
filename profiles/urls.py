from . import views
from .views import profile_page, edit_profile
from django.urls import path

urlpatterns = [
    path("", views.profile_page, name="profile_page"),
    path("edit/", views.edit_profile, name="edit_profile"),
    path("delete/", views.delete_profile, name="delete_profile"),
]