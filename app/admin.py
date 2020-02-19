from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Evaluation, Map, Place, Tag, User

# Register your models here.


class MapAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Map, MapAdmin)
admin.site.register(Tag)
admin.site.register(Place)
admin.site.register(Evaluation)
