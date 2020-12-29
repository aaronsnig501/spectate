from django.db import models
from sports.models import Sport


class Market(models.Model):

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="markets")

    def __str__(self):
        return f"{self.name}"
