from uuid import UUID
from urllib.parse import urlencode, urljoin

from django.shortcuts import get_object_or_404
from django.urls import reverse
import coreapi
import coreschema
from rest_framework import serializers, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.schemas import AutoSchema

from .models import Map, Place


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ("uuid", "name")
        fields = ("uuid", "name", "url_place_list")

    url_place_list = serializers.SerializerMethodField()

    def get_url_place_list(self, obj):
        return urljoin(reverse("place-list"), "?" + urlencode({"map_uuid": obj.uuid}))


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ("uuid", "name", "latitude", "longitude")


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
    queryset = Place.objects.filter(map__visibility=Map.Visibility.public.name)
    serializer_class = PlaceSerializer


class PlaceListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Return places belonging to the specified map_uuid.
    """

    permission_classes = (AllowAny,)
    serializer_class = PlaceSerializer
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "map_uuid",
                required=True,
                location="query",
                schema=coreschema.String(
                    title="uuid", description="A UUID string identifying the map."
                ),
            )
        ]
    )

    def get_queryset(self):
        try:
            map_uuid = UUID(self.request.query_params["map_uuid"])
        except KeyError:
            raise ParseError("Missing map_uuid filter")
        except ValueError:
            raise ParseError("map_uuid is not a valid UUID")

        try:
            map = Map.public.get(uuid=map_uuid)
        except Map.DoesNotExist:
            raise NotFound("Map not found")

        return Place.objects.filter(map=map)


api_router = SimpleRouter()
api_router.register("map", MapViewSet)
api_router.register("place", PlaceListViewSet, basename="place")
api_router.register("place", PlaceRetrieveViewSet, basename="place")
