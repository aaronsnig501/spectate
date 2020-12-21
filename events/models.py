from django.db import models
from django.conf import settings
from sports.models import Sport
from markets.models import Market


BASE_URL = f"http://{settings.ALLOWED_HOSTS[0]}:8000"


class Event(models.Model):
    """Event model"""

    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    sport = models.ForeignKey(Sport, on_delete=models.DO_NOTHING)
    markets = models.ForeignKey(Market, on_delete=models.DO_NOTHING)

    @property
    def url(self):
        return f"{BASE_URL}/matches/{self.id}"

    def __str__(self):
        return f"{self.name} ({self.sport.name}) - {self.start_time}"
