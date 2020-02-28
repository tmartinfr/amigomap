import enum
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import (
    PROTECT,
    Avg,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    EmailField,
    ForeignKey,
    IntegerField,
    Manager,
    ManyToManyField,
    Max,
    Min,
    Model,
    SlugField,
    TextField,
    UUIDField,
)

from .fields import ColorField
from .managers import FilterManager, UserManager


class BaseModelMixin(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        related_name="+",
        null=True,
    )

    # Populated by PostgreSQL triggers.
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        abstract = True


class User(BaseModelMixin, PermissionsMixin, AbstractBaseUser):
    email = EmailField(unique=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()


class Map(BaseModelMixin, Model):
    class Visibility(enum.Enum):
        public = "Public"
        private = "Private"

    visibility = CharField(
        max_length=32,
        choices=[(v.name, v.value) for v in Visibility],
        default=Visibility.private.name,
    )
    admin = ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="+", blank=True
    )
    viewer = ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="+", blank=True
    )
    name = CharField(max_length=255)
    slug = SlugField(max_length=50, unique=True)

    objects = Manager()
    public = FilterManager({"visibility": Visibility.public.name})

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def center(self):
        coord = self.places.aggregate(Avg("longitude"), Avg("latitude"))
        return (coord["latitude__avg"], coord["longitude__avg"])

    def bounds(self):
        """
        Returns tuple of top-left and bottom-right map corners.
        """
        bounds = self.places.aggregate(
            Min("longitude"),
            Min("latitude"),
            Max("longitude"),
            Max("latitude"),
        )
        return (
            (bounds["latitude__max"], bounds["longitude__min"]),
            (bounds["latitude__min"], bounds["longitude__max"]),
        )


class Tag(BaseModelMixin, Model):
    map = ForeignKey(Map, on_delete=PROTECT)
    name = CharField(max_length=255)
    color = ColorField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Place(BaseModelMixin, Model):
    map = ForeignKey(Map, on_delete=PROTECT, related_name="places")
    tag = ManyToManyField(Tag, blank=True)
    name = CharField(max_length=255)
    latitude = DecimalField(max_digits=9, decimal_places=7)
    longitude = DecimalField(max_digits=10, decimal_places=7)
    google_place_id = CharField(max_length=1024, null=True, blank=True)

    objects = Manager()
    public = FilterManager({"map__visibility": Map.Visibility.public.name})

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def note_mean(self):
        avg = self.evaluation_set.aggregate(Avg("note"))["note__avg"]
        if not avg:
            return None
        return int(avg)


class Evaluation(BaseModelMixin, Model):
    place = ForeignKey(Place, on_delete=PROTECT)
    note = IntegerField()
    comment = TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "Evaluation of {} by {}".format(
            self.place.name, self.creator.email
        )
