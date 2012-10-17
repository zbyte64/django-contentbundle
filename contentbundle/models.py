from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from contentbundle.adaptors import default_adaptors


class TypeInheritanceMixin(models.Model):
    model_type = models.CharField(max_length=64, blank=True, editable=False)
    
    @property
    def content_object(self):
        '''
        The implemented product
        Usually we are most interested in the object this returns
        '''
        name = self.model_type
        if name:
            return getattr(self, name, None)
        return None
    
    def lookup_model_type(self):
        one_to_one_fields = list()
        
        for field in self._meta.get_all_related_objects():
            if isinstance(field.field, models.OneToOneField):
                if hasattr(self, field.get_cache_name()):
                    return field.var_name
                one_to_one_fields.append(field)
        
        for field in one_to_one_fields:
            try:
                obj = field.model._base_manager.select_related().get(**{field.field.name:self.pk})
                setattr(self, field.get_cache_name(), obj)
                return field.var_name
            except ObjectDoesNotExist:
                pass
            except AttributeError:
                pass
        
        return ''
    
    def save(self, *args, **kwargs):
        if not self.model_type:
            self.model_type = self.lookup_model_type()
        return super(TypeInheritanceMixin, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True

class Remote(TypeInheritanceMixin):
    """
    A source for pushing and pulling bundles
    """
    @property
    def remote_type(self):
        return self.model_type

class BundleExportManifest(TypeInheritanceMixin):
    """
    Represents a configured bundle for exporting
    """
    @property
    def bundle_type(self):
        return self.model_type
    
    def commit(self, handler, adaptor):
        raise NotImplementedError

class BundleImportManifest(TypeInheritanceMixin):
    """
    Represents a configured bundle for exporting
    """
    @property
    def bundle_type(self):
        return self.model_type
    
    def clone(self, handler, adaptor):
        raise NotImplementedError

class AbstractRequest(models.Model):
    format = models.CharField(max_length=50, choices=default_adaptors.choices())
    
    handler_class = None
    
    def get_handler_class(self):
        return self.handler_class
    
    def get_handler_kwargs(self):
        return {}
    
    def get_handler(self):
        return self.get_handler_class()(**self.get_handler_kwargs())
    
    def get_adaptor(self):
        return default_adaptors.get_adaptor(self.format)
    
    class Meta:
        abstract = True

class PushRequest(AbstractRequest):
    remote = models.ForeignKey(Remote, related_name='push_requests')
    bundle_manifest = models.ForeignKey(BundleExportManifest, related_name='push_requests')
    
    def get_commit_kwargs(self):
        return {'handler':self.get_handler(),
                'adaptor':self.get_adaptor(),}
    
    def commit_data(self):
        self.bundle_manifest.commit(**self.get_commit_kwargs())

class PullRequest(AbstractRequest):
    remote = models.ForeignKey(Remote, related_name='pull_requests')
    bundle_manifest = models.ForeignKey(BundleImportManifest, related_name='push_requests')
    
    def get_clone_kwargs(self):
        return {'handler':self.get_handler(),
                'adaptor':self.get_adaptor(),}
    
    def clone_data(self):
        return self.bundle_manifest.clone(**self.get_clone_kwargs())

