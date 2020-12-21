from django.db import models


class Event(models.Model):
    """Event model"""

    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.name} - {self.start_time}"
