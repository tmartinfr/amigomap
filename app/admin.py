from django.contrib import admin

from .models import Map, Tag, Place, Evaluation

# Register your models here.


admin.site.register(Map)
admin.site.register(Tag)
admin.site.register(Place)
admin.site.register(Evaluation)
