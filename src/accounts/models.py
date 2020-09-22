from django.db import models
from django.conf import settings


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True
    )
    name = models.CharField(max_length=128, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
