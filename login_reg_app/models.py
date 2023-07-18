from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime as dt, timedelta as td
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def register_validator(self, postData, edit_profile=False, change_password=False):
        errors = {}
        if edit_profile:
            if len(postData["first_name"]) < 2:
                errors["first_name"] = "Your first name must be at least two characters"
            if len(postData["last_name"]) < 2:
                errors["last_name"] = "Your last name must be at least two characters"

            try:
                validate_email(postData["email"])
                is_unique = User.objects.filter(email=postData["email"])
                if is_unique:
                    errors[
                        "email"
                    ] = "This email is already taken.  Please use a different email."
            except ValidationError as e:
                errors["email"] = f"Incorrect email: {e}"
            username_unique = User.objects.filter(username=postData["username"])
            if username_unique:
                errors[
                    "username"
                ] = "This username is already taken.  Please use a different username."

            birthday = dt.strptime(postData["birthday"], "%Y-%M-%d")
            valid_birthday = dt.now() - td(days=13 * 365)
            if valid_birthday < birthday:
                errors[
                    "birthday"
                ] = "You are too young to register an account.  You must be at least 13 years old"
        if change_password:
            if postData["password"] != postData["pw_confirm"]:
                errors["pw_confirm"] = "Please enter the same password in PW Confirm"
            if len(postData["password"]) < 8:
                errors[
                    "password"
                ] = "Please enter a password that is at least 8 characters"
        return errors

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_("Users must have an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """Create and save a SuperUser with the given email and password."""
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True, default=None)
    friends = models.ManyToManyField("User", related_name="user_friends")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
