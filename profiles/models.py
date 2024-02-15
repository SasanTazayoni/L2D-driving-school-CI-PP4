from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=False, null=False)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    profile_picture = CloudinaryField('image', null=True, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    about_me = models.TextField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.username
