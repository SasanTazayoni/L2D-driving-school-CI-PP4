from .models import Comment
from django import forms
from django.forms import ModelForm
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)