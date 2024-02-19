from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from reviews.models import Review
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    email = forms.CharField(max_length=256)

    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'age', 'occupation', 'email', 'about_me', 'profile_picture']
