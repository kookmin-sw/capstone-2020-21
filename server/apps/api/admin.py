from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'gender', 'birthday', 'is_staff', 'is_active',)
    list_filter = ('gender', 'birthday', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'birthday', 'gender')}),
        ('Permissions', {'fields':('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'birthday', 'gender','is_staff', 'is_active')
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    
admin.site.register(User, CustomUserAdmin)
