from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from reviews.models import Review
from django.forms import ModelForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'profile_picture', 'about_me')


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']

