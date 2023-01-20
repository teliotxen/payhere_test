from django.db import models


class Item(models.Model):
    user = models.IntegerField()
    amount = models.IntegerField()
    note = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

