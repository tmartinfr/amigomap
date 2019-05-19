from typing import Any
from urllib.parse import urlencode, urljoin

from django.urls import reverse
from rest_framework import serializers

from ..models import Map, Place


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ("uuid", "name", "url_place_list", "center")

    url_place_list: Any = serializers.SerializerMethodField()

    def get_url_place_list(self, obj: Map) -> str:
        return urljoin(
            reverse("place-list"), "?" + urlencode({"map_uuid": obj.uuid})
        )


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ("uuid", "name", "latitude", "longitude")
