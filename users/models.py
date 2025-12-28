from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    username = models.CharField(verbose_name="Имя пользователя", blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    telegram_chat_id = models.CharField(max_length=32, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email