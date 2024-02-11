from . import views
from .views import profile_page, edit_profile
from django.urls import path

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register_user, name="register"),
    path("", views.profile_page, name="profile_page"),
    path("edit/", views.edit_profile, name="edit_profile"),
    path("delete/", views.delete_profile, name="delete_profile"),
]