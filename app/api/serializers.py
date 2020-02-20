from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from ..models import Map, Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "name", "latitude", "longitude", "note_mean")


class MapSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Map
        fields = ("id", "name", "center", "bounds")
        expandable_fields = {"places": (PlaceSerializer, {"many": True})}
