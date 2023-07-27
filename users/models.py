from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phone_field import PhoneField
from django.db import models
from uuid import uuid4

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    telegram_id = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    uniq_id = models.CharField(max_length=40, default=uuid4)
    confirm_email = models.CharField(max_length=10, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)




class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    phone = PhoneField()
    message = models.TextField()

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    image = models.ImageField(default='img')  #default rasm mondan darkor
    location = models.URLField(blank=True, null=True, default='https://goo.gl/maps/4J5Y1X6Z1Z2Z2Z2Z2')
#





