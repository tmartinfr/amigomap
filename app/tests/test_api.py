from collections import OrderedDict
from typing import Any

from django.test import Client, TestCase
from rest_framework import status

from ..factories import EvaluationFactory, MapFactory, PlaceFactory


class MapApiTest(TestCase):
    def test_bydomain(self) -> None:
        map = MapFactory(slug="resto")
        PlaceFactory(map=map, latitude=2, longitude=2)

        c = Client()
        resp: Any = c.get("/api/maps/bydomain/", HTTP_HOST="resto.localhost")
        expected_data = {
            "id": str(map.id),
            "name": map.name,
            "places": "/api/places/?map_id={}".format(map.id),
            "center": (2, 2),
            "bounds": ((2, 2), (2, 2)),
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, expected_data)


class PlaceApiTest(TestCase):
    def test_list(self) -> None:
        map = MapFactory(slug="resto")
        places = PlaceFactory.create_batch(3, map=map)

        c = Client()
        resp: Any = c.get(
            "/api/places/?map_id={}".format(map.id),
            HTTP_HOST="resto.localhost",
        )

        expected_data = [
            OrderedDict(
                [
                    ("id", str(place.id)),
                    ("name", place.name),
                    ("latitude", "{:.7f}".format(place.latitude)),
                    ("longitude", "{:.7f}".format(place.longitude)),
                    ("note_mean", None),
                ]
            )
            for place in reversed(places)
        ]
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, expected_data)

    def test_retrieve_without_note(self) -> None:
        map = MapFactory(slug="resto")
        place = PlaceFactory.create(map=map)

        c = Client()
        resp: Any = c.get(
            "/api/places/{}/".format(place.id), HTTP_HOST="resto.localhost"
        )

        expected_data = OrderedDict(
            [
                ("id", str(place.id)),
                ("name", place.name),
                ("latitude", "{:.7f}".format(place.latitude)),
                ("longitude", "{:.7f}".format(place.longitude)),
                ("note_mean", None),
            ]
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, expected_data)

    def test_retrieve_with_note(self) -> None:
        map = MapFactory(slug="resto")
        place = PlaceFactory.create(map=map)
        EvaluationFactory.create(place=place, note=6)
        EvaluationFactory.create(place=place, note=2)

        c = Client()
        resp: Any = c.get(
            "/api/places/{}/".format(place.id), HTTP_HOST="resto.localhost"
        )

        expected_data = OrderedDict(
            [
                ("id", str(place.id)),
                ("name", place.name),
                ("latitude", "{:.7f}".format(place.latitude)),
                ("longitude", "{:.7f}".format(place.longitude)),
                ("note_mean", 4),
            ]
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, expected_data)
