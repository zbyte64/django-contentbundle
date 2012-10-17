class AdaptorRegistry(dict):
    def get_adaptor(self, format):
        return self[format]
    
    def regster_adaptor(self, format, adaptor):
        self[format] = adaptor
    
    def choices(self):
        return zip(self.keys(), self.keys())

default_adaptors = AdaptorRegistry()

class Adaptor(object):
    """
    Adaptors serialize and deserialize basic python data structures and django file objects
    """
    format = None
    
    def serialize(self, handler, path, python_objects):
        raise NotImplementedError
    
    def deserialize(self, handler, path):
        raise NotImplementedError
    
    @classmethod
    def register_adaptor(cls):
        default_adaptors.register_adaptor(cls.format, cls)

from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder

class JSONAdaptor(Adaptor):
    format = 'json'
    
    #TODO media/file handling
    
    def serialize(self, handler, path, python_objects):
         data = simplejson.dumps(python_objects, cls=DjangoJSONEncoder)
         handler.write_data(path, data)
    
    def deserialize(self, handler, path):
        data = handler.get_data(path)
        return simplejson.load(data)

JSONAdaptor.register_adaptor()
