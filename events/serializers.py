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
    message_type = CharField(write_only=True)

    class Meta:
        fields = "__all__"
        model = Event

    def message_type_is_valid(self, message_type):
        """Message type is invalid

        A small helper method to ensure that the `message_type` has a message of either
        "NewEvent" or "UpdateOdds"

        Args:
            message_type (str): The message_type provided by the client

        Returns:
            bool: True if message_type is "NewEvent" or "UpdateOdds". Otherwise False.
        """
        if not (message_type == "NewEvent" or message_type == "UpdateOdds"):
            return False
        else:
            return True

    def can_proceed_to_create_event(self, message_type, id):
        """Can proceed to create event

        Ensures that the incoming data has a `message_type` of "NewEvent" and doesn't
        already exist in the database

        Args:
            message_type (str): The `message_type` provided by the client
            id (int): The `id` of the event provided by the client

        Returns:
            bool: True if message is "NewEvent" and the Event doesn't already exist.
                  Otherwise False
        """
        if message_type == "NewEvent" and Event.objects.filter(id=id).exists():
            return False
        else:
            return True

    def selection_is_invalid(self, data, participants):
        """Selection is invalid

        A simple helper method used to determine if the data coming from the client
        contains the correct number of participants for that sport

        Args:
            data (Selection): The Selection to be validated
            participants (int): The number of participants allowed

        Returns:
            bool: False if the length of data not equal to the number of participants.
                  Otherwise True
        """
        return len(data) != participants

    def to_representation(self, instance):
        """To representation

        Override the default representation to retrieve all of the markets for sport
        of the current event.
        """
        data = super(EventSerializer, self).to_representation(instance)
        data["markets"] = MarketSerializer(instance.sport.markets.all(), many=True).data
        return data

    def get_validated_selection_data(self, market):
        """Get validated selection data

        Helper method to retrieve all of the selections provided by the client

        Args:
            market (list): The validated market data

        Returns:
            list: The validated selections
        """
        validated_selection_data = [
            selection for market in market for selection in market["selections"]
        ]
        return validated_selection_data

    def get_or_create_markets_with_selections(self, market_data, sport):
        """Get or create markets with selections

        If a specific market doesn't exist then it will need to be created, as it will
        need to be referenced when creating the selections. This will create the market
        for every market provide, along with its selections.

        If the markets already exist then they will just be retrieved from the database
        as normal.

        Args:
            market_data (list): The validated market data
            sport (Sport): The instance of the sport object
        """
        for market_data in market_data:
            market, _ = Market.objects.get_or_create(
                id=market_data["id"],
                defaults={
                    "id": market_data["id"],
                    "name": market_data["name"],
                    "sport": sport,
                },
            )
            for selection in market_data["selections"]:
                selection = Selection.objects.create(
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
        message_type = validated_data.pop("message_type")
        validated_sport_data = validated_data.pop("sport")
        validated_market_data = validated_data.pop("markets")
        validated_selection_data = self.get_validated_selection_data(
            validated_market_data
        )

        if not self.message_type_is_valid(message_type):
            raise ValidationError(
                "Unknown message_type. Try again with either `NewEvent` or `UpdateOdds`"
            )

        sport = Sport.objects.get(name=validated_sport_data["name"])
        markets = Market.objects.filter(sport=sport)

        if message_type == "UpdateOdds":
            for selection in validated_selection_data:
                event_selection = Selection.objects.get(id=selection["id"])
                event_selection.odds = selection["odds"]
                event_selection.save()

            return Event.objects.get(id=id)

        if not self.can_proceed_to_create_event(message_type, id):
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
