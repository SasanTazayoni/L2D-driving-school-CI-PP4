from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    username = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    profile_picture = CloudinaryField('image', null=True)
    about_me = models.TextField(blank=False, null=True)
    has_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username