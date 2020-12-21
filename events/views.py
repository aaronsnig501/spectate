from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer


class EventsAPI(APIView):
    """Events API View"""

    serializer_class = EventSerializer

    def get(self, request, pk, **kwargs):
        """GET request handler"""
        event = Event.objects.get(id=pk)
        serializer = self.serializer_class(event)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
