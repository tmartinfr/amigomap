import enum
import uuid

from django.contrib.auth.models import User
from django.db import models

from model_utils.models import TimeStampedModel, SoftDeletableModel


class BaseModel(TimeStampedModel, SoftDeletableModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    creator = models.ForeignKey(User, on_delete=models.PROTECT,
                                related_name='+')

    class Meta:
        abstract = True


class Map(BaseModel):

    class Visibility(enum.Enum):
        public = 'Public'
        private = 'Private'

    visibility = models.CharField(
        max_length=32, choices=[(v.name, v.value) for v in Visibility],
        default=Visibility.private.name)
    admin = models.ManyToManyField(User, related_name='+', blank=True)
    viewer = models.ManyToManyField(User, related_name='+', blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Place(BaseModel):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    def __str__(self):
        return self.name


class Evaluation(BaseModel):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    note = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return '{} by {}'.format(self.place.name, self.creator.username)
