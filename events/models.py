from django.db import models
from django.conf import settings
from sports.models import Sport
from markets.models import Market


class Event(models.Model):
    """Event model"""

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    sport = models.ForeignKey(Sport, on_delete=models.DO_NOTHING)

    @property
    def url(self):
        return f"{settings.CURRENT_DOMAIN}/api/match/{self.id}"

    def __str__(self):
        return f"{self.name} ({self.sport.name}) - {self.start_time}"
