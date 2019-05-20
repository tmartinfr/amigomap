from typing import Any
from urllib.parse import urlencode, urljoin

from django.urls import reverse
from rest_framework import serializers

from ..models import Map, Place


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ("id", "name", "url_place_list", "center", "bounds")

    url_place_list: Any = serializers.SerializerMethodField()

    def get_url_place_list(self, obj: Map) -> str:
        return urljoin(
            reverse("place-list"), "?" + urlencode({"map_id": obj.id})
        )


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "name", "latitude", "longitude")
