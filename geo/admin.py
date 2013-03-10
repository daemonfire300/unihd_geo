from django.contrib.gis import admin
from geo.models import Street, Building
from geo.models import Playground

admin.site.register(Street, admin.OSMGeoAdmin)
admin.site.register(Playground, admin.OSMGeoAdmin)
admin.site.register(Building, admin.OSMGeoAdmin)