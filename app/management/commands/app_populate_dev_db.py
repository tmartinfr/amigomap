from django.core.management.base import BaseCommand

from ...factories import UserFactory, MapFactory, PlaceFactory


class Command(BaseCommand):
    """
    Populate database with an admin/admin user and a few maps with fixed slugs.
    This command should not crash is entries are already existing, but is not
    idempotent.
    """

    MAP_SLUGS = ("resto", "coworking", "running")

    def _create_admin(self):
        admin = UserFactory.create(is_staff=True, is_superuser=True, username="admin")
        admin.set_password("admin")
        admin.save()
        return admin

    def _create_map(self, slug, creator):
        return MapFactory.create(slug=slug, name=slug.capitalize(), creator=creator)

    def _create_place(self, map, creator):
        PlaceFactory.create(map=map, creator=creator)

    def handle(self, *args, **kwargs):
        admin = self._create_admin()
        for slug in self.MAP_SLUGS:
            map = self._create_map(slug, admin)
            for _ in range(100):
                self._create_place(map, admin)
            self.stdout.write(
                "Generating map http://{}.localhost:8000/".format(map.slug)
            )
