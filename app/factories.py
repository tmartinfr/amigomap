import factory
from slugify import slugify

from . import models


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ('username',)

    username = factory.Faker('sha1')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class MapFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Map
        django_get_or_create = ('slug',)

    creator = factory.SubFactory(UserFactory)
    name = factory.Faker('city')
    visibility = models.Map.Visibility.public.name
    slug = factory.LazyAttribute(lambda o: slugify(o.name))


class PlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Place

    creator = factory.SubFactory(UserFactory)
    map = factory.SubFactory(MapFactory)
    name = factory.Faker('company')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
