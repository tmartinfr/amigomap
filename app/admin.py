from django.contrib import admin

from .models import PlaceMap, Tag, Place, Evaluation

# Register your models here.


admin.site.register(PlaceMap)
admin.site.register(Tag)
admin.site.register(Place)
admin.site.register(Evaluation)
