from collections import OrderedDict
from uuid import uuid4

from django.test import Client, TestCase
from rest_framework import status

from ..factories import EvaluationFactory, MapFactory, PlaceFactory


class MapApiTest(TestCase):
    def setUp(self):
        self.map = MapFactory(slug="resto")
        self.place = PlaceFactory(map=self.map, latitude=2, longitude=2)

    @classmethod
    def _expected_data(cls, map, expand=False):
        data = OrderedDict(
            (
                ("id", str(map.id)),
                ("name", map.name),
                ("center", (2, 2)),
                ("bounds", ((2, 2), (2, 2))),
            )
        )
        if expand:
            data.update(
                places=[PlaceApiTest._expected_data(map.places.first())]
            )
        return data

    def test_retrieve(self):
        c = Client()
        resp = c.get(f"/api/maps/{self.map.id}/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, self._expected_data(self.map))

    def test_retrieve_expand(self):
        c = Client()
        resp = c.get(f"/api/maps/{self.map.id}/?expand=places")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, self._expected_data(self.map, expand=True))

    def test_bydomain(self):
        c = Client()
        resp = c.get("/api/maps/bydomain/", HTTP_HOST="resto.localhost")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, self._expected_data(self.map))

    def test_bydomain_expand(self):
        c = Client()
        resp = c.get(
            "/api/maps/bydomain/?expand=places", HTTP_HOST="resto.localhost"
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, self._expected_data(self.map, expand=True))


class PlaceApiTest(TestCase):
    @classmethod
    def _expected_data(cls, place):
        return OrderedDict(
            (
                ("id", str(place.id)),
                ("name", place.name),
                ("latitude", "{:.7f}".format(place.latitude)),
                ("longitude", "{:.7f}".format(place.longitude)),
                ("note_mean", None),
            )
        )

    def test_list(self):
        map = MapFactory(slug="resto")
        places = PlaceFactory.create_batch(3, map=map)

        c = Client()
        resp = c.get(
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

    def test_retrieve_without_note(self):
        map = MapFactory(slug="resto")
        place = PlaceFactory.create(map=map)

        c = Client()
        resp = c.get(
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

    def test_retrieve_with_note(self):
        map = MapFactory(slug="resto")
        place = PlaceFactory.create(map=map)
        EvaluationFactory.create(place=place, note=6)
        EvaluationFactory.create(place=place, note=2)

        c = Client()
        resp = c.get(
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

    def test_list_missing_map_id(self):
        c = Client()
        resp = c.get("/api/places/", HTTP_HOST="resto.localhost")

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.json(), {"detail": "Missing map_id filter"})

    def test_list_map_id_not_json(self):
        c = Client()
        resp = c.get(
            "/api/places/?map_id={}".format("42"), HTTP_HOST="resto.localhost"
        )

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.json(), {"detail": "map_id is not a valid UUID"})

    def test_list_map_id_not_found(self):
        c = Client()
        resp = c.get(
            "/api/places/?map_id={}".format(uuid4()),
            HTTP_HOST="resto.localhost",
        )

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.json(), {"detail": "Map not found"})
