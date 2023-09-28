from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_id = models.IntegerField(default=0)


class TgUser(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    telegram_id = models.IntegerField()
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True, null=True)
    token = models.TextField(unique=True, blank=True, null=True)

