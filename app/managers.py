from django.db import models


class FilterManager(models.Manager):
    def __init__(self, filters):
        self.filters = filters
        return super().__init__()

    def get_queryset(self):
        return super().get_queryset().filter(**self.filters)
