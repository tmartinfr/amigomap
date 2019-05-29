from defusedxml import minidom
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from ...factories import MapFactory, PlaceFactory


class Command(BaseCommand):
    """
    Create new map based on a KML file.
    """

    def add_arguments(self, parser):
        parser.add_argument("kml_file", type=str)
        parser.add_argument("map_slug", type=str)
        parser.add_argument("creator_id", type=str)

    def _get_map_name(self, dom):
        document = dom.getElementsByTagName("Document")[0]
        return document.getElementsByTagName("name")[0].firstChild.data.strip()

    def _get_place_coordinates(self, placemark):
        point = placemark.getElementsByTagName("Point")[0]
        coordinates = point.getElementsByTagName("coordinates")[0]
        return reversed(coordinates.firstChild.data.strip().split(",")[:2])

    def _get_place_name(self, placemark):
        tag = placemark.getElementsByTagName("name")[0]
        return tag.firstChild.data.strip()

    def _get_places(self, dom):
        places = []
        for placemark in dom.getElementsByTagName("Placemark"):
            name = self._get_place_name(placemark)
            latitude, longitude = self._get_place_coordinates(placemark)
            places.append((name, latitude, longitude))
        return places

    def _create(self, map_name, map_slug, places, creator):
        map = MapFactory.create(slug=map_slug, name=map_name, creator=creator)
        for place in places:
            PlaceFactory.create(
                map=map,
                creator=creator,
                name=place[0],
                latitude=place[1],
                longitude=place[2],
            )

    def handle(self, *args, **options):
        creator = User.objects.get(id=options["creator_id"])
        dom = minidom.parse(options["kml_file"])
        map_name = self._get_map_name(dom)
        places = self._get_places(dom)
        self._create(map_name, options["map_slug"], places, creator)
