# Generated by Django 4.2.9 on 2024-02-22 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_remove_userprofile_email_and_more'),
        ('reviews', '0004_review_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='user_reviews', to='profiles.userprofile'),
        ),
    ]