from rest_framework.serializers import ModelSerializer
from .models import Event
from sports.serializers import SportSerializer
from markets.serializers import MarketSerializer


class EventListSerializer(ModelSerializer):
    class Meta:
        fields = ["id", "url", "name", "start_time"]
        model = Event


class EventSerializer(ModelSerializer):

    sport = SportSerializer()
    markets = MarketSerializer()

    class Meta:
        fields = ["id", "url", "name", "start_time", "sport", "markets"]
        model = Event