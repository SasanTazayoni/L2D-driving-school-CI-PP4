from django.contrib import admin
from .models import UserProfile
from django_summernote.admin import SummernoteModelAdmin


@admin.register(UserProfile)
class UserProfileAdmin(SummernoteModelAdmin):
    """
    Custom admin panel for managing user profiles.
    """
    list_display = ('get_name', 'created_on', 'approved')
    search_fields = ['user__first_name', 'about_me']
    summernote_fields = ('about_me',)
    actions = ['approve_profiles']

    def get_name(self, obj):
        return obj.user.first_name
    get_name.short_description = 'Name'

    def approve_profiles(self, request, queryset):
        updated_count = queryset.update(approved=True)
        self.message_user(request, f'{updated_count} profiles have been approved.')