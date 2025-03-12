from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Child

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'role', 'email', 'is_staff')

admin.site.register(User, CustomUserAdmin)

admin.site.register(Child)