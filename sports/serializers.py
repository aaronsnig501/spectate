from rest_framework import serializers
from .models import Sport


class SportSerializer(serializers.ModelSerializer):
    """Sport serializer"""

    class Meta:
        fields = ["id", "name"]
        model = Sport