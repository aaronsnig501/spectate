from rest_framework.serializers import ModelSerializer, CharField
from .models import Selection


class SelectionSerializer(ModelSerializer):

    id = CharField(validators=[])

    class Meta:
        fields = ["id", "name", "odds"]
        model = Selection
