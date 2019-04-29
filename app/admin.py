from django.contrib import admin

from .models import Evaluation, Map, Place, Tag

# Register your models here.


class MapAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Map, MapAdmin)
admin.site.register(Tag)
admin.site.register(Place)
admin.site.register(Evaluation)
