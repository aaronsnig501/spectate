from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import ValidationError
from .models import Event
from .utils import filter_by_params, parse_query_params
from .serializers import EventSerializer, EventListSerializer


class EventsAPI(GenericAPIView):
    """Events API View"""

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ["start_time", "name", "id"]
    ordering = ["-start_time"]

    def get(self, request, pk=None, **kwargs):
        """GET request handler

        Handles incoming GET requests for the `matches` endpoint. This handles two
        potential requests, both the details view and the list view.

        If a `pk` is provided, only the instance that has that ID will be returned,
        otherwise a list will be returned, filtered and ordered according to the request
        params.

        Example:
            Detail View:
                curl http://127.0.0.1:8000/api/match/6

            Response:
                {
                    "id": 6,
                    "url": "http://127.0.0.1:8000/matches/6",
                    "name": "Real Madrid vs Barcelona",
                    "startTime": "2020-12-21T22:03:30Z",
                    "sport": {
                        "id": 1,
                        "name": "Football"
                    },
                    "markets": {
                        "id": 7,
                        "name": "Winner",
                        "selections": [
                            {
                                "id": 15,
                                "name": "Real Madrid",
                                "odds": 10
                            },
                            {
                                "id": 16,
                                "name": "Barcelona",
                                "odds": 5.55
                            }
                        ]
                    }
                }

            List View:
                curl http://127.0.0.1:8000/api/match/

            Response:
                [
                    {
                        "id": 3,
                        "url": "http://127.0.0.1:8000/matches/3",
                        "name": "Real Madrid vs Barcelona",
                        "startTime": "2020-12-21T22:03:30Z"
                    },
                    {
                        "id": 4,
                        "url": "http://127.0.0.1:8000/matches/4",
                        "name": "Real Madrid vs Barcelona",
                        "startTime": "2020-12-21T22:03:30Z"
                    },
                    {
                        "id": 5,
                        "url": "http://127.0.0.1:8000/matches/5",
                        "name": "Real Madrid vs Barcelona",
                        "startTime": "2020-12-21T22:03:30Z"
                    },
                    {
                        "id": 6,
                        "url": "http://127.0.0.1:8000/matches/6",
                        "name": "Real Madrid vs Barcelona",
                        "startTime": "2020-12-21T22:03:30Z"
                    }
                ]

        """
        if pk:
            try:
                event = Event.objects.get(id=pk)
                serializer = self.serializer_class(event)
            except Event.DoesNotExist:
                return Response(
                    {"message": f"Event with ID of {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            params = parse_query_params(request)
            events = self.filter_queryset(self.queryset)
            events = filter_by_params(events, params)
            serializer = EventListSerializer(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        """POST request handler

        This endpoint will be used with two specific goals in mind. The first is to
        create new events, and the second is to update the odds of a specific event.

        This is accomplished using specific messages. The two types of messages
        expected are:
            `NewEvent`: Indicates that a new event is to be created
            `UpdateOdds`: Indicates that the odds on an events selections are to be
                          updated

        Example Usage:
            curl -X POST -H "Content-type: application/json" http://127.0.0.1:8000/api/match/ -d \
                '{
                    "id": 1,
                    "message":"NewEvent",
                    "name": "Real Madrid vs Barcelona",
                    "startTime": "2020-12-21T22:03:30Z",
                    "sport": {"id": 1, "name": "Football"},
                    "markets": {
                        "id": 1,
                        "name": "Winner",
                        "selections": [
                            {
                                "id": 1,
                                "name": "Real Madrid",
                                "odds": 10
                            },
                            {
                                "id": 2,
                                "name": "Barcelona",
                                "odds": 5.55
                            }
                        ]
                    }
                }'
        """
        event_serializer = self.serializer_class(data=request.data)

        if event_serializer.is_valid():
            if event_serializer.validated_data["message"] == "NewEvent":
                try:
                    event_serializer.save()
                except ValidationError as e:
                    return Response(
                        data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(event_serializer.data, status=status.HTTP_201_CREATED)
            elif event_serializer.validated_data["message"] == "UpdateOdds":
                event = event_serializer.save()
                updated_event = self.serializer_class(event)
                return Response(updated_event.data, status=status.HTTP_200_OK)
            else:
                message = (
                    "Unknown message. Try again with either `NewEvent` or `UpdateOdds`"
                )
                return Response(
                    data={"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
