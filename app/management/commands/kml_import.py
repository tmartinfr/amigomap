from defusedxml import minidom
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...factories import MapFactory, PlaceFactory


class Command(BaseCommand):
    """
    Create new map based on a KML file.
    """

    def add_arguments(self, parser):
        parser.add_argument("kml_file", type=str)
        parser.add_argument("map_slug", type=str)
        parser.add_argument("creator_email", type=str)

    def _get_map_name(self, dom):
        document = dom.getElementsByTagName("Document")[0]
        return str(
            document.getElementsByTagName("name")[0].firstChild.data.strip()
        )

    def _get_place_coordinates(self, placemark):
        point = placemark.getElementsByTagName("Point")[0]
        coordinates = point.getElementsByTagName("coordinates")[0]
        longitude, latitude, _ = coordinates.firstChild.data.strip().split(",")
        return (latitude, longitude)

    def _get_place_name(self, placemark):
        tag = placemark.getElementsByTagName("name")[0]
        return str(tag.firstChild.data.strip())

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
        creator = get_user_model().objects.get(email=options["creator_email"])
        dom = minidom.parse(options["kml_file"])
        map_name = self._get_map_name(dom)
        places = self._get_places(dom)
        self._create(map_name, options["map_slug"], places, creator)
