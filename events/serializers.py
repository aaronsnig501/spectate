from rest_framework.serializers import ModelSerializer, CharField
from .models import Event
from sports.models import Sport
from sports.serializers import SportSerializer
from markets.models import Market
from markets.serializers import MarketSerializer
from selections.models import Selection


class EventListSerializer(ModelSerializer):
    """Event List Serializer

    The amount of data that we need when getting a list of events is less than the
    amount of information needed for an individual item. For this reason, we have this
    separate serializer for when we need to view the truncated data
    """

    class Meta:
        fields = ["id", "url", "name", "start_time"]
        model = Event


class EventSerializer(ModelSerializer):
    """Event Serializer

    This serializer will be used to get all information related to an individual event.
    This will be used for both detail views, and creating new events.

    This serializer also has one additional piece of information, which is the `message`
    field. This will be used to determine what the client is expecting to accomplish
    when posting data.
    """

    id = CharField(validators=[])
    sport = SportSerializer()
    markets = MarketSerializer()
    message = CharField(required=False)

    class Meta:
        fields = ["id", "url", "name", "start_time", "sport", "markets", "message"]
        model = Event

    def create(self, validated_data):
        """Create Event

        When creating a new event we want to create a new event, with an existing sport,
        and as the odds will be specific to an event we should create new a new `market`
        with `selection` objects for each team or player.

        First we'll extract the data from the `validated_data` dict parameter, then get
        the correlating `Sport` and create a new `Market` with a `Selection` for each item
        in the `selections` list. This information will then be used create and save
        the new event

        Args:
            validated_data (dict): The dict implicitly passed when `.save()` is called

        Returns:
            Event: The newly created `Event` instance
        """
        id = validated_data.pop("id")
        name = validated_data.pop("name")
        start_time = validated_data.pop("start_time")
        validated_sport_data = validated_data.pop("sport")
        validated_market_data = validated_data.pop("markets")
        validated_selection_data = validated_market_data.pop("selections")

        sport = Sport.objects.get(name=validated_sport_data["name"])
        market = Market.objects.create(
            id=validated_market_data["id"], name=validated_market_data["name"]
        )

        selections = [
            Selection.objects.create(
                id=selection["id"],
                name=selection["name"],
                odds=selection["odds"],
                markets=market,
            )
            for selection in validated_selection_data
        ]

        event = Event(
            id=id, name=name, start_time=start_time, sport=sport, markets=market
        )
        event.save()
        return event

    def update_selections(self):
        """Update selections

        Update the odds of each selection
        """
        event = Event.objects.get(id=self.validated_data["id"])
        selections = self.validated_data["markets"]["selections"]

        for selection in selections:
            event_selection = event.markets.selections.get(id=selection["id"])
            event_selection.odds = selection["odds"]
            event_selection.save()
