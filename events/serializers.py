from rest_framework import serializers
from .models import Event
from sports.serializers import SportSerializer


class EventSerializer(serializers.ModelSerializer):

    sport = SportSerializer()

    class Meta:
        fields = ["id", "url", "name", "sport"]
        model = Event
