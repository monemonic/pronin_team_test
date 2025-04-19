from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active'
    )
    list_filter = ('is_staff', 'is_superuser',)
