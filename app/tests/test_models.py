from typing import Any

from django.test import TestCase

from ..factories import MapFactory
from ..models import Map


class MapModelTest(TestCase):
    def test_visibility(self) -> None:
        """
        Test Map.public()
        """
        MapFactory.create_batch(3, visibility=Map.Visibility.public.name)
        self.assertEqual(Map.public.count(), 3)

        map: Any = Map.public.first()
        map.visibility = Map.Visibility.private.name
        map.save()

        self.assertEqual(Map.public.count(), 2)
        self.assertNotIn(map, Map.public.all())
