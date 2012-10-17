from django.core.files.base import ContentFile

class RemoteHandler(object):
    def get_data(self, path):
        return self.get_media(path).read()
    
    def get_media(self, path):
        return NotImplementedError
    
    def write_media(self, path, file_obj):
        return NotImplementedError
    
    def write_data(self, path, data):
        return self.write_media(path, ContentFile(data))
