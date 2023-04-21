from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.conf import settings
import os


def get_default_image_path():
    return os.path.join('default.jpg')


class User(AbstractBaseUser, PermissionsMixin):
    # phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    profile = models.ImageField(default='default.jpg')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.id}'

    @property
    def is_staff(self):
        return self.is_superuser
