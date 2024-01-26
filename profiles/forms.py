from .models import UserProfile
from django import forms


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'profile_picture', 'about_me')


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm