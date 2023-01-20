from django.db import models


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)