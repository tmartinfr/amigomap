from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        raise NotImplementedError

    def create_superuser(self, email, password):
        raise NotImplementedError


class FilterManager(models.Manager):
    def __init__(self, filters):
        self.filters = filters
        return super().__init__()

    def get_queryset(self):
        return super().get_queryset().filter(**self.filters)
