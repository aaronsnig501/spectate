from django.db import models
from markets.models import Market


class Selection(models.Model):

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    odds = models.FloatField()
    markets = models.ForeignKey(
        Market, on_delete=models.DO_NOTHING, related_name="selections"
    )

    def __str__(self):
        return f"{self.name} ({self.odds})"