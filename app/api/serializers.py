from typing import Any
from urllib.parse import urlencode, urljoin

from django.urls import reverse
from rest_framework import serializers

from ..models import Map, Place


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ("id", "name", "places", "center", "bounds")

    places: Any = serializers.SerializerMethodField()

    def get_places(self, obj: Map) -> str:
        return urljoin(
            reverse("places-list"), "?" + urlencode({"map_id": obj.id})
        )


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "name", "latitude", "longitude")
