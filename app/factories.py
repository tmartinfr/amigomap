import factory
from . import models


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker('sha1')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class MapFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Map

    creator = factory.SubFactory(UserFactory)
    name = factory.Faker('city')
    visibility = models.Map.Visibility.public.name


class PlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Place

    creator = factory.SubFactory(UserFactory)
    map = factory.SubFactory(MapFactory)
    name = factory.Faker('company')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
