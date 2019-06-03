from typing import Any, List, Tuple

from defusedxml import minidom
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandParser

from ...factories import MapFactory, PlaceFactory

Places = List[Tuple[str, str, str]]


class Command(BaseCommand):
    """
    Create new map based on a KML file.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("kml_file", type=str)
        parser.add_argument("map_slug", type=str)
        parser.add_argument("creator_id", type=str)

    def _get_map_name(self, dom: Any) -> str:
        document = dom.getElementsByTagName("Document")[0]
        return str(
            document.getElementsByTagName("name")[0].firstChild.data.strip()
        )

    def _get_place_coordinates(self, placemark: Any) -> Tuple[str, str]:
        point = placemark.getElementsByTagName("Point")[0]
        coordinates = point.getElementsByTagName("coordinates")[0]
        longitude, latitude, _ = coordinates.firstChild.data.strip().split(",")
        return (latitude, longitude)

    def _get_place_name(self, placemark: Any) -> str:
        tag = placemark.getElementsByTagName("name")[0]
        return str(tag.firstChild.data.strip())

    def _get_places(self, dom: Any) -> Places:
        places = []
        for placemark in dom.getElementsByTagName("Placemark"):
            name = self._get_place_name(placemark)
            latitude, longitude = self._get_place_coordinates(placemark)
            places.append((name, latitude, longitude))
        return places

    def _create(
        self, map_name: str, map_slug: str, places: Places, creator: User
    ) -> None:
        map = MapFactory.create(slug=map_slug, name=map_name, creator=creator)
        for place in places:
            PlaceFactory.create(
                map=map,
                creator=creator,
                name=place[0],
                latitude=place[1],
                longitude=place[2],
            )

    def handle(self, *args: None, **options: str) -> None:
        creator = User.objects.get(id=options["creator_id"])
        dom = minidom.parse(options["kml_file"])
        map_name = self._get_map_name(dom)
        places = self._get_places(dom)
        self._create(map_name, options["map_slug"], places, creator)
