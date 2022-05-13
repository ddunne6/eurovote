from django.db import models

class Setting(models.Model):
    allow_new_users = models.BooleanField()