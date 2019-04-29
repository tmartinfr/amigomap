from rest_framework.routers import SimpleRouter

from .viewsets import MapViewSet, PlaceListViewSet, PlaceRetrieveViewSet

api_router = SimpleRouter()
api_router.register("map", MapViewSet)
api_router.register("place", PlaceListViewSet, basename="place")
api_router.register("place", PlaceRetrieveViewSet, basename="place")
