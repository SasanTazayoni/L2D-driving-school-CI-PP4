"""
URL configuration for l2d project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core import views as core_views


urlpatterns = [
    path("", core_views.home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("appointments/", core_views.appointments, name="appointments"),
    path("contact/", core_views.contact, name="contact"),
    path("profile/", include("profiles.urls"), name="profile"),
    path("reviews/", include("reviews.urls"), name="reviews"),
    path("summernote/", include("django_summernote.urls")),
    path("user-profiles/", include("core.urls"), name="user-profiles"),
]
