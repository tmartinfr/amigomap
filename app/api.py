from rest_framework import serializers, viewsets, mixins
from rest_framework_nested import routers

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
    queryset = Map.objects.filter(visibility=Map.Visibility.public.name)
    serializer_class = MapSerializer


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        return Place.objects.filter(map=self.kwargs['map_pk'])


main_router = routers.SimpleRouter()
main_router.register('map', MapViewSet)

map_router = routers.NestedSimpleRouter(main_router, 'map', lookup='map')
map_router.register('place', PlaceViewSet, base_name='map-place')
