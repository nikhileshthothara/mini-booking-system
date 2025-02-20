from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authbase.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("id", "email", "is_active", "is_staff", "is_superuser", "created_at")
    list_filter = ("is_active", "is_staff", "is_superuser", "created_at")
    search_fields = ("email",)
    ordering = ("-created_at",)
    list_per_page = 20

    fieldsets = (
        ("Personal Info", {"fields": ("email", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")