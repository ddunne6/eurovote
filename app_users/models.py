from django.db import models

ALLOW_NEW_USERS = "Allow new users to sign up"

class Setting(models.Model):
    name = models.CharField(max_length=100)
    enable = models.BooleanField()

    def __str__(self) -> str:
        return self.name