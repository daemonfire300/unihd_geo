#class GeoRouter(object):
#    def db_for_read(self, model, **hints):
#        if model._meta.app_label == 'geo':
#            return 'geo'
#        return None
#    
#    def db_for_write(self, model, **hints):
#        if model._meta.app_label == 'geo':
#            return 'geo'
#        return None
#    
#    def allow_relation(self, obj1, obj2, **hints):
#        if obj1._meta.app_label == 'geo' or obj2._meta.app_label == 'geo':
#            return True
#        return None
#    
#    def allow_syncdb(self, db, model):
#        if db == 'geo':
#            return model._meta.app_label == 'geo'
#        elif model._meta.app_label == 'geo':
#            return False
#        return None