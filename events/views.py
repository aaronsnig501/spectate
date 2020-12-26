from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .utils import filter_by_params, parse_query_params
from .serializers import EventSerializer, EventListSerializer


class EventsAPI(APIView):
    """Events API View"""

    serializer_class = EventSerializer

    def get(self, request, pk=None, **kwargs):
        """GET request handler"""
        if pk:
            event = Event.objects.get(id=pk)
            serializer = self.serializer_class(event)
        else:
            params = parse_query_params(request)
            events = filter_by_params(Event.objects.all(), params)
            serializer = EventListSerializer(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        """POST request handler"""
        event_serializer = self.serializer_class(data=request.data)

        if event_serializer.is_valid():
            if event_serializer.validated_data["message"] == "NewEvent":
                event_serializer.save()
        else:
            print(event_serializer.errors)
        return Response({"hello": "message"})
