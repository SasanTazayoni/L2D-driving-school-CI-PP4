# Generated by Django 4.2.9 on 2024-02-05 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_userprofile_about_me_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about_me',
            field=models.TextField(blank=True, help_text='Write a short description about yourself or just say hello...', max_length=200, null=True),
        ),
    ]
