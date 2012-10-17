class RemoteHandler(object):
    def get_data(self, path):
        return NotImplementedError
    
    def get_media(self, path):
        return NotImplementedError
    
    def write_media(self, path, file_obj):
        return NotImplementedError
    
    def write_data(self, path, data):
        return NotImplementedError
