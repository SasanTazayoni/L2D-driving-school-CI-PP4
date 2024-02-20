from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserProfile
from reviews.models import Review
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label="Name", max_length=30)

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Please choose a different username")
        return username

    class Meta:
        model = User
        fields = ['first_name','username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    first_name = forms.CharField(label="Name", max_length=30)

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'age', 'occupation', 'about_me', 'profile_picture']
