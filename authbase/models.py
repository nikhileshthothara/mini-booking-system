from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from .validator import Validator


class User(AbstractUser):
    """
        Inheriting AbstractUser Model to provide future compatibility in terms
        of adding extra fields etc
        NOTE: Kept Email as the username field.
    """
    username = None
    email = models.EmailField(
        max_length=200, unique=True, db_index=True, validators=[
            Validator.unique_email_validator])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # NOTE: Custom object manager, also to provide expansion
    objects = UserManager()

    def __str__(self):
        return f"User: {self.email} ID: {self.id}"
