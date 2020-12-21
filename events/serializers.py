from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.Serializer):

    name = serializers.CharField()
    start_time = serializers.DateTimeField()