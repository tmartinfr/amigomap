from django.test import TestCase

from ..factories import (
    EvaluationFactory,
    MapFactory,
    PlaceFactory,
    TagFactory,
    UserFactory,
)
from ..models import Map


class MapModelTest(TestCase):
    def test_str(self):
        map = MapFactory(name="Aix")
        self.assertEqual(str(map), "Aix")

    def test_visibility(self):
        MapFactory.create_batch(3, visibility=Map.Visibility.public.name)
        self.assertEqual(Map.public.count(), 3)

        map = Map.public.first()
        map.visibility = Map.Visibility.private.name
        map.save()

        self.assertEqual(Map.public.count(), 2)
        self.assertNotIn(map, Map.public.all())

    def test_center(self):
        map = MapFactory.create()
        PlaceFactory.create(map=map, latitude=2, longitude=6)
        PlaceFactory.create(map=map, latitude=8, longitude=2)
        PlaceFactory.create(map=map, latitude=9, longitude=12)
        PlaceFactory.create(map=map, latitude=11, longitude=4)
        self.assertEqual(map.center(), (7.5, 6))

    def test_bounds(self):
        map = MapFactory.create()
        PlaceFactory.create(map=map, latitude=2, longitude=6)
        PlaceFactory.create(map=map, latitude=8, longitude=2)
        PlaceFactory.create(map=map, latitude=9, longitude=12)
        PlaceFactory.create(map=map, latitude=11, longitude=4)
        self.assertEqual(map.bounds(), ((11, 2), (2, 12)))


class TagModelTest(TestCase):
    def test_str(self):
        tag = TagFactory(name="Restaurant")
        self.assertEqual(str(tag), "Restaurant")


class PlaceModelTest(TestCase):
    def test_str(self):
        place = PlaceFactory(name="Restaurant")
        self.assertEqual(str(place), "Restaurant")


class EvaluationModelTest(TestCase):
    def test_str(self):
        place = PlaceFactory(name="Chez Nino")
        creator = UserFactory(username="rico")
        evaluation = EvaluationFactory(creator=creator, place=place)
        self.assertEqual(str(evaluation), "Evaluation of Chez Nino by rico")
