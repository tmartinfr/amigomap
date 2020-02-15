import enum
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Max, Min
from model_utils.models import SoftDeletableModel, TimeStampedModel

from .fields import ColorField
from .managers import FilterManager


class BaseModel(TimeStampedModel, SoftDeletableModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="+"
    )

    class Meta:
        abstract = True


class Map(BaseModel):
    class Visibility(enum.Enum):
        public = "Public"
        private = "Private"

    visibility = models.CharField(
        max_length=32,
        choices=[(v.name, v.value) for v in Visibility],
        default=Visibility.private.name,
    )
    admin = models.ManyToManyField(User, related_name="+", blank=True)
    viewer = models.ManyToManyField(User, related_name="+", blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)

    objects = models.Manager()
    public = FilterManager({"visibility": Visibility.public.name})

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name

    def center(self):
        coord = self.place_set.aggregate(Avg("longitude"), Avg("latitude"))
        return (coord["latitude__avg"], coord["longitude__avg"])

    def bounds(self):
        """
        Returns tuple of top-left and bottom-right map corners.
        """
        bounds = self.place_set.aggregate(
            Min("longitude"),
            Min("latitude"),
            Max("longitude"),
            Max("latitude"),
        )
        return (
            (bounds["latitude__max"], bounds["longitude__min"]),
            (bounds["latitude__min"], bounds["longitude__max"]),
        )


class Tag(BaseModel):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    color = ColorField()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name


class Place(BaseModel):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    google_place_id = models.CharField(max_length=1024, null=True, blank=True)

    objects = models.Manager()
    public = FilterManager({"map__visibility": Map.Visibility.public.name})

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name

    def note_mean(self):
        avg = self.evaluation_set.aggregate(Avg("note"))["note__avg"]
        if not avg:
            return None
        return int(avg)


class Evaluation(BaseModel):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    note = models.IntegerField()
    comment = models.TextField()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return "Evaluation of {} by {}".format(
            self.place.name, self.creator.username
        )
