from django.test import Client, TestCase
from rest_framework import status

from ..factories import MapFactory, PlaceFactory


class MapApiTest(TestCase):
    def test_payload(self) -> None:
        map = MapFactory(slug="resto")
        PlaceFactory(map=map, latitude=2, longitude=2)

        c = Client()
        resp = c.get("/api/maps/bydomain/", HTTP_HOST="resto.localhost")
        expected_data = {
            "id": str(map.id),
            "name": map.name,
            "places": "/api/places/?map_id={}".format(map.id),
            "center": (2, 2),
            "bounds": ((2, 2), (2, 2)),
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, expected_data)
