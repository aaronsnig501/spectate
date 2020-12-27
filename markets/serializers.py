from rest_framework.serializers import ModelSerializer, CharField
from .models import Market
from selections.serializers import SelectionSerializer


class MarketSerializer(ModelSerializer):

    id = CharField(validators=[])
    selections = SelectionSerializer(many=True)

    class Meta:
        fields = ["id", "name", "selections"]
        model = Market