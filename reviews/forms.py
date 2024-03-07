from .models import Comment
from django import forms
from django.forms import ModelForm
from .models import Review


class ReviewForm(ModelForm):
    """
    Form for creating or updating a review.
    """
    class Meta:
        model = Review
        fields = ['rating', 'content']


class CommentForm(forms.ModelForm):
    """
    Form for creating a comment on a review.
    """
    class Meta:
        model = Comment
        fields = ('content',)