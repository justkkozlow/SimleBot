from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_name = models.CharField(max_length=256)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Staff"


class Clients(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name
