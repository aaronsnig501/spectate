from django.db import models


class Selection(models.Model):

    name = models.CharField(max_length=255)
    odds = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.odds})"