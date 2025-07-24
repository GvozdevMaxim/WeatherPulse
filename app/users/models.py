from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    telegram_id = models.BigIntegerField(blank=True,
                                         null=True,
                                         unique=True)
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def has_telegram(self):
        return self.telegram_id is not None

