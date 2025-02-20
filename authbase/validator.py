from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class Validator:
    """
        Centralised validator for all auth related stuff.
    """
    @staticmethod
    def unique_email_validator(value):
        from authbase.models import User
        try:
            validate_email(value)
            if User.objects.filter(email=value).exists():
                raise ValidationError("User with email already exists.")
        except ValidationError as e:
            raise ValidationError(e)
        return True

    @staticmethod
    def password_validator(value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValidationError(e)
        return True
