from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter

from .models import Map, Place


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('uuid', 'name',)


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('uuid', 'name', 'latitude', 'longitude')


class MapViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Map.public.all()
    serializer_class = MapSerializer

    @action(detail=False)
    def bydomain(self, request):
        map_slug = request.META['HTTP_HOST'].split('.')[0]
        map = get_object_or_404(Map, slug=map_slug)
        serializer = MapSerializer(map)
        return Response(serializer.data)


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        try:
            map_uuid = UUID(self.request.query_params['map_id'])
        except KeyError:
            raise ParseError('Missing map_id filter')
        except ValueError:
            raise ParseError('map_id is not a valid UUID')

        try:
            map = Map.public.get(uuid=map_uuid)
        except Map.DoesNotExist:
            raise NotFound('Map not found')

        return Place.objects.filter(map=map)


api_router = SimpleRouter()
api_router.register('map', MapViewSet)
api_router.register('place', PlaceViewSet, basename='place')
