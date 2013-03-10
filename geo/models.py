from django.contrib.gis.db import models

class Street(models.Model):
    name = models.CharField(max_length=128)
    lstring = models.LineStringField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
class Playground(models.Model):
    name = models.CharField(max_length=128)
    area = models.PolygonField()
    objects = models.GeoManager()
    
class Building(models.Model):
    name = models.CharField(max_length=128)
    hash = models.CharField(max_length=232)
    poly = models.PolygonField()
    objects = models.GeoManager()