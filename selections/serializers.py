from rest_framework.serializers import ModelSerializer
from .models import Selection


class SelectionSerializer(ModelSerializer):
    class Meta:
        fields = ["id", "name", "odds"]
        model = Selection