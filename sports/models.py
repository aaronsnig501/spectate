from django.db import models


class Sport(models.Model):

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
