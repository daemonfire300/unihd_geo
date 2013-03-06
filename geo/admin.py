from django.contrib.gis import admin
from geo.models import Street
from geo.models import Playground

admin.site.register(Street, admin.OSMGeoAdmin)
admin.site.register(Playground, admin.OSMGeoAdmin)