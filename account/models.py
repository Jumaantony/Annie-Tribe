from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone = models.TextField(max_length=20, blank=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile for user {self.username}'
