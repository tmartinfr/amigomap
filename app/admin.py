from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Evaluation, Map, Place, Tag, User

# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "updated_at")


class MapAdmin(BaseAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.unregister(Group)
admin.site.register(User, BaseAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Tag, BaseAdmin)
admin.site.register(Place, BaseAdmin)
admin.site.register(Evaluation, BaseAdmin)
