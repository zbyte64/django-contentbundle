from hyperadmin.resources.crud.crud import CRUDResource
from hyperadmin.resources.resources import Resource

class PushRequestResource(Resource):
    #add & detail only
    pass

class BundleExportManifestResource(CRUDResource):
    push_request_resource_class = PushRequestResource
    
    def get_item_push_links(self, item):
        if item.instance.manifest is None:
            pass #TODO return add links
        else:
            pass #TODO return detail link for existing manifest

class PullRequestResource(Resource):
    #add & detail only
    pass

class RemoteResource(CRUDResource):
    pull_request_resource_class = PullRequestResource
