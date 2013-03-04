from django.contrib.gis import admin
from geo.models import Street

admin.site.register(Street, admin.OSMGeoAdmin)