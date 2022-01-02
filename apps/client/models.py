from uuid import uuid4

from django.db import models


# Create your models here.

class Client(models.Model):
    """Client model for saving information of client in bank """

    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'