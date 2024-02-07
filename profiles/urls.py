from . import views
from .views import profile_page, edit_profile
from django.urls import path

urlpatterns = [
    path("login/", views.userLogin, name="login"),
    path("logout/", views.userLogout, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("", views.profile_page, name="profile_page"),
    path("edit/", views.edit_profile, name="edit_profile"),
]