from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# -------- Custom User Admin --------
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    ordering = ['-date_joined']

    # remove groups/permissions references
    filter_horizontal = ()
    list_filter = ('is_active', 'is_staff', 'is_admin')
    fieldsets = ()

# -------- User Profile Admin --------
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country', 'created_at')
    search_fields = ('user__email', 'user__username', 'city', 'country')
    readonly_fields = ('created_at', 'modified')

# -------- Register Admin Models --------
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
