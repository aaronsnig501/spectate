from rest_framework.serializers import Serializer, ModelSerializer, CharField
from rest_framework.exceptions import ValidationError
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
    markets = MarketSerializer(many=True, required=False)
    message = CharField(write_only=True)

    class Meta:
        fields = "__all__"
        model = Event

    def can_proceed_to_create_event(self, message, id):
        if message == "NewEvent" and Event.objects.filter(id=id).exists():
            return False
        else:
            return True

    def selection_is_invalid(self, data, participants):
        return len(data) != participants

    def to_representation(self, instance):
        data = super(EventSerializer, self).to_representation(instance)
        data["markets"] = MarketSerializer(instance.sport.markets.all(), many=True).data
        return data

    def get_validated_selection_data(self, market):
        validated_selection_data = [
            selection for market in market for selection in market["selections"]
        ]
        return validated_selection_data

    def get_or_create_markets_with_selections(self, market_data, sport):
        for market_data in market_data:
            market, _ = Market.objects.get_or_create(
                id=market_data["id"],
                defaults={
                    "id": market_data["id"],
                    "name": market_data["name"],
                    "sport": sport,
                },
            )
            if not len(market_data["selections"]) >= sport.number_of_participants:
                for selection in market_data["selections"]:
                    Selection.objects.create(
                        id=selection["id"],
                        name=selection["name"],
                        odds=selection["odds"],
                        markets=market,
                    )

    def create(self, validated_data):
        """Create Event

        When creating a new event we want to create a new event, with an existing sport,
        and as the odds will be specific to an event we should create new a new `market`
        with `selection` objects for each team or player.

        First we'll extract the data from the `validated_data` dict parameter, then get
        the correlating `Sport` and create a new `Market` with a `Selection` for each item
        in the `selections` list. This information will then be used create and save
        the new event.

        It will also throw a validation error if the client passes a number of selections
        not equal to the number of `sport.number_of_participants`.

        Args:
            validated_data (dict): The dict implicitly passed when `.save()` is called

        Returns:
            Event: The newly created `Event` instance
        """
        id = validated_data.pop("id")
        name = validated_data.pop("name")
        start_time = validated_data.pop("start_time")
        message = validated_data.pop("message")
        validated_sport_data = validated_data.pop("sport")
        validated_market_data = validated_data.pop("markets")
        validated_selection_data = self.get_validated_selection_data(
            validated_market_data
        )

        sport = Sport.objects.get(name=validated_sport_data["name"])
        markets = Market.objects.filter(sport=sport)

        if not self.can_proceed_to_create_event(message, id):
            raise ValidationError(
                f"Event with ID {id} already exists. Try updating the odds"
            )

        if self.selection_is_invalid(
            validated_selection_data, sport.number_of_participants
        ):
            raise ValidationError(
                (
                    f"{sport.name} requires {sport.number_of_participants} participants."
                    f"You have provided {len(validated_selection_data)}"
                )
            )

        markets = self.get_or_create_markets_with_selections(
            validated_market_data, sport
        )

        event = Event(id=id, name=name, start_time=start_time, sport=sport)
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
