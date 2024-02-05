from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', null=False, blank=False)
    username = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    profile_picture = CloudinaryField('image', null=True, blank=True)
    about_me = models.TextField(max_length=200, blank=True, null=True, help_text="Write a short description about yourself or just say hello...")
    has_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()