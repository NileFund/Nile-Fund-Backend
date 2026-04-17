from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    
    fieldsets = (
        ('Personal Info', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone', 'profile_picture',
                'birthdate', 'facebook_profile', 'country'
            )
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'phone'),
        }),
    )
    
    search_fields = ('email', 'phone')
    ordering = ('email',)