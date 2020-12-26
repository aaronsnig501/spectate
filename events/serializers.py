from rest_framework.serializers import ModelSerializer, CharField
from .models import Event
from sports.models import Sport
from sports.serializers import SportSerializer
from markets.models import Market
from markets.serializers import MarketSerializer
from selections.models import Selection


class EventListSerializer(ModelSerializer):
    class Meta:
        fields = ["id", "url", "name", "start_time"]
        model = Event


class EventSerializer(ModelSerializer):

    sport = SportSerializer()
    markets = MarketSerializer()
    message = CharField(required=False)

    class Meta:
        fields = ["id", "url", "name", "start_time", "sport", "markets", "message"]
        model = Event

    def create(self, validated_data):
        name = validated_data.pop("name")
        start_time = validated_data.pop("start_time")
        validated_sport_data = validated_data.pop("sport")
        validated_market_data = validated_data.pop("markets")
        validated_selection_data = validated_market_data.pop("selections")

        sport = Sport.objects.get(name=validated_sport_data["name"])
        market = Market.objects.filter(name=validated_market_data["name"])

        selections = [
            Selection(name=selection["name"], odds=selection["odds"], markets=market)
            for selection in validated_selection_data
        ]
        selections = Selection.objects.bulk_create(selections)

        event = Event(name=name, start_time=start_time, sport=sport, markets=market)
        event.save()
        return event
