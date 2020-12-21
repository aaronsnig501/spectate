from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer


class EventsAPI(APIView):
    """Events API View"""

    serializer_class = EventSerializer

    def get(self, request, pk=None, **kwargs):
        """GET request handler"""
        if pk:
            event = Event.objects.get(id=pk)
            serializer = self.serializer_class(event)
        else:
            events = Event.objects.all()

            # Get query strings
            sport = request.GET.get("sport", None)
            name = request.GET.get("name", None)

            # Query string filters
            if sport is not None:
                events = events.filter(sport__name__iexact=sport)
            if name is not None:
                events = events.filter(name__iexact=name)

            serializer = self.serializer_class(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
