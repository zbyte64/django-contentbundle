import os

from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from contentbundle.models import Remote, PullRequest, PushRequest
from contentbundle.handler import RemoteHandler


class StorageHandler(RemoteHandler):
    def __init__(self, storage, path, format):
        self.storage = storage
        self.path = path
        super(StorageHandler, self).__init__()
    
    def path_join(self, path):
        #TODO paths need to be sanitized
        return os.path.join(self.path, path)
    
    def get_data(self, path):
        path = self.path_join(path)
        return self.storage.open(path, 'r').read()
    
    def get_media(self, path):
        path = self.path_join(path)
        return self.storage.open(path, 'r')
    
    def write_media(self, path, file_obj):
        path = self.path_join(path)
        return self.storage.save(path, file_obj)
    
    def write_data(self, path, data):
        path = self.path_join(path)
        return self.storage.save(path, ContentFile(data))

def get_storages():
    return []

class StorageRemote(Remote):
    storage_backends = models.CharField(max_length=256, choices=get_storages(), blank=True) #place holder
    folder = models.CharField(max_length=256)
    
    @property
    def storage(self):
        return default_storage
    
    def get_push_request_class(self):
        return MediaStoragePushRequest
    
    def get_pull_request_class(self):
        return MediaStoragePullRequest

class MediaStoragePushRequest(PushRequest):
    path = models.CharField(max_length=256)
    
    storage_handler_class = StorageHandler
    
    def get_storage_handler_kwargs(self):
        return {'storage':self.remote.storage,
                'path':self.path,}
    
    def clean_remote(self):
        if not isinstance(self.remote, StorageRemote):
            raise ValidationError('Invalid remote type')

class MediaStoragePullRequest(PullRequest):
    path = models.CharField(max_length=256)
    
    storage_handler_class = StorageHandler
    
    def get_storage_handler_kwargs(self):
        return {'storage':self.remote.storage,
                'path':self.path,}
    
    def clean_remote(self):
        if not isinstance(self.remote, StorageRemote):
            raise ValidationError('Invalid remote type')

