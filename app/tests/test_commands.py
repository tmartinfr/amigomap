from typing import Any

from decimal import Decimal
from io import StringIO
from tempfile import NamedTemporaryFile

from django.core.management import call_command
from django.test import TestCase

from ..factories import UserFactory
from ..models import Map


class CommandsTest(TestCase):
    def test_app_populate_dev_db(self) -> None:
        out = StringIO()

        call_command("app_populate_dev_db", stdout=out)

        expected_output = "".join(
            [
                "Generating map http://{}.localhost:8000/\n".format(slug)
                for slug in ("resto", "coworking", "running")
            ]
        )
        self.assertEqual(out.getvalue(), expected_output)

    def test_kml_import(self) -> None:
        out = StringIO()
        user = UserFactory.create()
        kml_file = NamedTemporaryFile(suffix=".kml")
        kml_file.write(
            b"""<?xml version="1.0" encoding="UTF-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2">
            <Document>
                <name>Resto map</name>
                <Folder>
                    <name>Restaurants</name>
                    <Placemark>
                        <name>
                        Piadina
                        </name>
                        <styleUrl>#icon-1899-0F9D58-nodesc</styleUrl>
                        <Point>
                        <coordinates>
                            5.4523033,43.5259687,0
                        </coordinates>
                        </Point>
                    </Placemark>
                    <Placemark>
                        <name>Le bourbi</name>
                        <styleUrl>#icon-1899-F9A825-nodesc</styleUrl>
                        <Point>
                        <coordinates>
                            5.4487842,43.5262575,0
                        </coordinates>
                        </Point>
                    </Placemark>
                    <Placemark>
                        <name>Pousse au crime</name>
                        <styleUrl>#icon-1899-A52714-nodesc</styleUrl>
                        <Point>
                        <coordinates>
                            5.4541111,43.5266387,0
                        </coordinates>
                        </Point>
                    </Placemark>
                </Folder>
            </Document>
            </kml>
        """
        )
        kml_file.flush()

        call_command(
            "kml_import", kml_file.name, "testmap", user.id, stdout=out
        )

        self.assertEqual(out.getvalue(), "")
        map: Any = Map.objects.first()
        self.assertEqual(map.name, "Resto map")
        expected_places = [
            ("Pousse au crime", Decimal("43.5266387"), Decimal("5.4541111")),
            ("Le bourbi", Decimal("43.5262575"), Decimal("5.4487842")),
            ("Piadina", Decimal("43.5259687"), Decimal("5.4523033")),
        ]
        self.assertListEqual(
            list(map.place_set.values_list("name", "latitude", "longitude")),
            expected_places,
        )
