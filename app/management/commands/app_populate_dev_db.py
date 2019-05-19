from django.core.management.base import BaseCommand

from ...factories import MapFactory, PlaceFactory, UserFactory


class Command(BaseCommand):
    """
    Populate database with an admin/admin user and a few maps with fixed slugs.
    This command should not crash is entries are already existing, but is not
    idempotent.
    """

    MAP_SLUGS = ("resto", "coworking", "running")

    AIX_PLACES = (
        ("Piadina", "43.529620", "5.444722"),
        ("Maison Nosh", "43.526788", "5.449337"),
        ("La Mie Dinette", "43.528581", "5.439296"),
    )

    def _create_admin(self):
        admin = UserFactory.create(
            is_staff=True, is_superuser=True, username="admin"
        )
        admin.set_password("admin")
        admin.save()
        return admin

    def _create_map(self, slug, creator):
        return MapFactory.create(
            slug=slug, name=slug.capitalize(), creator=creator
        )

    def _create_aix_map(self, admin):
        """
        Hidden Aix-en-Provence map!
        """
        map = self._create_map("aix", admin)
        for place in self.AIX_PLACES:
            PlaceFactory.create(
                map=map,
                creator=admin,
                name=place[0],
                latitude=place[1],
                longitude=place[2],
            )

    def handle(self, *args, **kwargs):
        admin = self._create_admin()
        for slug in self.MAP_SLUGS:
            map = self._create_map(slug, admin)
            for _ in range(100):
                PlaceFactory.create(map=map, creator=admin)
            self.stdout.write(
                "Generating map http://{}.localhost:8000/".format(map.slug)
            )
        self._create_aix_map(admin)
