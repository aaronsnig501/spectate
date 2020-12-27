from rest_framework.serializers import ModelSerializer, CharField
from .models import Sport


class SportSerializer(ModelSerializer):
    """Sport serializer"""

    id = CharField(validators=[])

    class Meta:
        fields = ["id", "name"]
        model = Sport