from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))
RATING_CHOICES = ((1, "1 star"), (2, "2 stars"), (3, "3 stars"), (4, "4 stars"), (5, "5 stars"))


# Create your models here.
class Review(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name="review", null=False, blank=False)
    rating = models.IntegerField(choices=RATING_CHOICES, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)