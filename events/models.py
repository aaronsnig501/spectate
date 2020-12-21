from django.db import models
from sports.models import Sport


class Event(models.Model):
    """Event model"""

    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    sport = models.ForeignKey(Sport, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name} ({self.sport.name}) - {self.start_time}"
