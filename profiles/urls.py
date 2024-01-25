from . import views
from .views import profile_page
from django.urls import path

urlpatterns = [
    path('', profile_page, name='profile_page'),
]