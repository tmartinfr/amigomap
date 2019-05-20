from rest_framework.routers import SimpleRouter

from .viewsets import MapViewSet, PlaceListViewSet, PlaceRetrieveViewSet

api_router = SimpleRouter()
api_router.register("maps", MapViewSet)
api_router.register("places", PlaceListViewSet, basename="places")
api_router.register("places", PlaceRetrieveViewSet, basename="places")
