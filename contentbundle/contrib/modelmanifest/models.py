from django.db import models
from django.db.models.loading import get_app, get_apps, get_models
from django.contrib.contenttypes.models import ContentType
from django.core import serializers as django_serializers

from contentbundle.models import BundleExportManifest, BundleImportManifest


class ModelBundleExportManifest(BundleExportManifest):
    use_natural_keys = models.BooleanField(default=True)
    
    object_sources = set()
    
    def get_all_objects(self):
        all_objects = list()
        for src in self.object_sources:
            entries = src.objects.filter(manifest_bundle=self)
            for entry in entries:
                all_objects.extend(entry.get_objects())
        return all_objects
    
    def get_file_objects_from_instance(self, instance):
        return []
    
    def commit(self, handler, adaptor):
        objects = self.get_all_objects()
        python_objects = django_serializers.serialize('python', objects, use_natural_keys=self.use_natural_keys)
        #unforunately this does not have any file objects, it needs to be processed seperately
        path = 'manifest.%s' % adaptor.format
        adaptor.serialize(handler, path, python_objects)
        for instance in objects:
            file_objects = self.get_file_objects_from_instance(instance)
            for file_obj in file_objects:
                path = file_obj.path #or name?
                handler.write_media(path, file_obj)

class ApplicationExport(models.Model):
    manifest_bundle = models.ForeignKey(ModelBundleExportManifest)
    application = models.CharField()
    
    def get_objects(self):
        objects = list()
        app = get_app(self.application)
        models = get_models(app)
        for model in models:
            objects.extend(model.objects.all())
        return objects

ModelBundleExportManifest.object_sources.add(ApplicationExport)


class ModelExport(models.Model):
    manifest_bundle = models.ForeignKey(ModelBundleExportManifest)
    content_type = models.ForeignKey(ContentType)
    
    def get_objects(self):
        model = self.content_type.model_class()
        return model.objects.all()

ModelBundleExportManifest.object_sources.add(ModelExport)


class ModelBundleImportManifest(BundleImportManifest):
    def clone(self, handler, adaptor):
        path = 'manifest.%s' % adaptor.format
        python_objects = adaptor.deserialize(handler, path)
        objects = django_serializers.deserialize('python', python_objects)
        
        results = list()
        for obj in objects:
            #TODO retrieve file objects
            obj.save()
            results.append(obj)
        return results

