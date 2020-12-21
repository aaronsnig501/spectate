from rest_framework.serializers import ModelSerializer
from .models import Selection


class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection