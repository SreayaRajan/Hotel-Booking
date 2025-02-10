from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)  # Email is required and unique
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Optional phone number

    
    def _str_(self):
        return self.email