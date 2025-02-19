from django.contrib import admin
from authbase.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass