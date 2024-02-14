from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            first_name=instance.first_name,
        )


@receiver(post_save, sender=UserProfile)
def update_user_profile(sender, instance, created, **kwargs):
    user = instance.user
    profile = instance

    if created == False:
        user.first_name = profile.first_name
        user.username = profile.username
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=UserProfile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()
