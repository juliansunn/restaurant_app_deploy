from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from login_reg_app.models import User

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    ordering = ("email",)
