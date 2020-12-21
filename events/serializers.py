from rest_framework.serializers import ModelSerializer
from .models import Event
from sports.serializers import SportSerializer
from markets.serializers import MarketSerializer


class EventSerializer(ModelSerializer):

    sport = SportSerializer()
    markets = MarketSerializer()

    class Meta:
        fields = "__all__"
        model = Event
