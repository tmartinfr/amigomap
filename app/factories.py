import factory
import factory.fuzzy
from django.conf import settings
from slugify import slugify

from . import models


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ("email",)

    email = factory.Faker("email")


class MapFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Map
        django_get_or_create = ("slug",)

    creator = factory.SubFactory(UserFactory)
    name = factory.Faker("city")
    visibility = models.Map.Visibility.public.name
    slug = factory.LazyAttribute(lambda o: slugify(o.name))


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Tag

    creator = factory.SubFactory(UserFactory)
    map = factory.SubFactory(MapFactory)


class PlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Place

    creator = factory.SubFactory(UserFactory)
    map = factory.SubFactory(MapFactory)
    name = factory.Faker("company")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")


class EvaluationFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Evaluation

    creator = factory.SubFactory(UserFactory)
    place = factory.SubFactory(PlaceFactory)
    note = factory.fuzzy.FuzzyInteger(0, 5)
    comment = factory.fuzzy.FuzzyText()
