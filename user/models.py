from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from phonenumbers import PhoneNumber
from phonenumbers.phonenumberutil import parse


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password"""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    GENDER_CHOICES = {
        "MALE": "Male",
        "FEMALE": "Female",
        "OTHER": "Other",
        "NOT PROVIDED": "Not provided",
    }

    username = None
    first_name = models.CharField(max_length=50)  # TODO: add validation and test it
    last_name = models.CharField(max_length=50)  # TODO: add validation and test it
    email = models.EmailField(_("email address"), unique=True)
    # Additional info about user
    gender = models.CharField(
        max_length=12, choices=GENDER_CHOICES, null=True, blank=True
    )
    birthday = models.DateTimeField(
        null=True, blank=True
    )  # TODO: add validation and test it
    phone_number = models.CharField(
        max_length=20, blank=True, null=True
    )  # TODO: test validation

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def clean(self):
        # Validate and normalize phone number
        if self.phone_number:
            try:
                parsed_number = parse(self.phone_number, None)
                self.phone_number = str(
                    PhoneNumber(
                        parsed_number.country_code, parsed_number.national_number
                    )
                )
            except Exception as e:
                raise ValidationError({"phone_number": [f"Invalid phone number: {e}"]})

    def __str__(self):
        return f"{self.get_full_name()} - {self.email}"
