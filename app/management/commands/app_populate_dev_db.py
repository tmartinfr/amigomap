from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from ...factories import (
    EvaluationFactory,
    MapFactory,
    PlaceFactory,
    UserFactory,
)
from ...models import Map


class Command(BaseCommand):
    """
    Populate database with an admin/admin user and a few maps with fixed slugs.
    This command should not crash is entries are already existing, but is not
    idempotent.
    """

    MAP_SLUGS = ("resto", "coworking", "running")

    AIX_PLACES = (
        ("Piadina", "43.529620", "5.444722", 10),
        ("Maison Nosh", "43.526788", "5.449337", 10),
        ("La Mie Dinette", "43.528581", "5.439296", 10),
        ("Sous les platanes", "43.529315", "5.449572", 5),
        ("Terminus", "43.531727", "5.447791", 5),
        ("Le bourbi", "43.523917", "5.452211", 2),
        ("Pousse au crime", "43.523574", "5.439723", 2),
    )

    def _create_admin(self) -> User:
        admin: User = UserFactory.create(
            is_staff=True, is_superuser=True, username="admin"
        )
        admin.set_password("admin")
        admin.save()
        return admin

    def _create_map(self, slug: str, creator: User) -> Map:
        map: Map = MapFactory.create(
            slug=slug, name=slug.capitalize(), creator=creator
        )
        return map

    def _create_aix_map(self, admin: User) -> None:
        """
        Hidden Aix-en-Provence map!
        """
        map = self._create_map("aix", admin)
        for place in self.AIX_PLACES:
            p = PlaceFactory.create(
                map=map,
                creator=admin,
                name=place[0],
                latitude=place[1],
                longitude=place[2],
            )
            EvaluationFactory.create(creator=admin, place=p, note=place[3])

    def handle(self, *args: None, **kwargs: None) -> None:
        admin = self._create_admin()
        for slug in self.MAP_SLUGS:
            map = self._create_map(slug, admin)
            for _ in range(100):
                PlaceFactory.create(map=map, creator=admin)
            self.stdout.write(
                "Generating map http://{}.localhost:8000/".format(map.slug)
            )
        self._create_aix_map(admin)
