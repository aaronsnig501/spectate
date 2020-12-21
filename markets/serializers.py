from rest_framework.serializers import ModelSerializer
from .models import Market


class MarketSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Market