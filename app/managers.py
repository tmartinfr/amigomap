from typing import Dict

from django.db import models
from django.db.models import QuerySet


class FilterManager(models.Manager):
    def __init__(self, filters: Dict[str, str]):
        self.filters = filters
        return super().__init__()

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(**self.filters)
