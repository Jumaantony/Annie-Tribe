from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(blank=True,
                              max_length=20,
                              choices=CHOICES)

    def __str__(self):
        return f'Profile for user {self.user.username}'