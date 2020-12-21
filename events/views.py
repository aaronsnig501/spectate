from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .utils import filters
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
            events = filters(Event.objects.all(), request)
            serializer = self.serializer_class(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
