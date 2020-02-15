from uuid import UUID

import coreapi
import coreschema
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from ..models import Map, Place
from .serializers import MapSerializer, PlaceSerializer


class MapViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Map.public.all()
    serializer_class = MapSerializer

    @action(detail=False)
    def bydomain(self, request):
        """
        Return map matching the request HTTP Host header.
        """
        map_slug = request.META["HTTP_HOST"].split(".")[0]
        map = get_object_or_404(Map, slug=map_slug)
        serializer = MapSerializer(map)
        return Response(serializer.data)


class PlaceRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Place.public.all()
    serializer_class = PlaceSerializer


class PlaceListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Return places belonging to the specified map_id.
    """

    permission_classes = (AllowAny,)
    serializer_class = PlaceSerializer
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "map_id",
                required=True,
                location="query",
                schema=coreschema.String(description="Map identifier"),
            )
        ]
    )

    def get_queryset(self):
        try:
            map_id = UUID(self.request.query_params["map_id"])
        except KeyError:
            raise ParseError("Missing map_id filter")
        except ValueError:
            raise ParseError("map_id is not a valid UUID")

        try:
            map = Map.public.get(id=map_id)
        except Map.DoesNotExist:
            raise NotFound("Map not found")

        return Place.public.filter(map=map)
