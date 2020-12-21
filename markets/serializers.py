from rest_framework.serializers import ModelSerializer
from .models import Market
from selections.serializers import SelectionSerializer


class MarketSerializer(ModelSerializer):

    selections = SelectionSerializer(many=True)

    class Meta:
        fields = ["id", "name", "selections"]
        model = Market