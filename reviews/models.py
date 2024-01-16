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

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Written by {self.author} on {self.created_on}"


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter",  null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    approved = models.BooleanField(default=False)
    replied_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-replied_on"]

    def __str__(self):
        return f"Written by {self.author} on {self.replied_on}"