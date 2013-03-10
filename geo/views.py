import urllib2
from common.http.jsonresponse import Success
from django.db import transaction
from geo.models import Building
from django.contrib.gis.geos import GEOSGeometry


def fetch_buildings(request):
    resp = urllib2.urlopen('http://129.206.228.72:8080/OSMGeometrieService/osmgeomservice/buildings/8.659085/49.390474/8.712819/49.434311')
    with transaction.commit_on_success():
        for line in resp:
            Building.objects.create(poly=GEOSGeometry(line))
    return Success({"nothing": "here"})
#{'hash': u'', 'name': u'', 'b_id': 3391, '_state': <django.db.models.base.ModelState object at 0x1db99d0>, 'poly': <Polygon object at 0x2047be0>, 'intersct': '0105000020E6100000020000000102000000020000002C2EE983C05D2140AE49B72572B748401B84B9DDCB5D21406CE45F7072B748400102000000020000001B84B9DDCB5D21406CE45F7072B748404C6B781FEC5D21405ABBED4273B74840', 'id': 3}