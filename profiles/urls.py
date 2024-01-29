from . import views
from .views import profile_page, edit_profile
from django.urls import path

urlpatterns = [
    path('', profile_page, name='profile_page'),
    path('edit/', edit_profile, name='edit_profile'),
]