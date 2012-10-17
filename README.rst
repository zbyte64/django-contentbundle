TODO, this is ALPHA

The following are development notes.

======
Models
======

BundleExportManifest
====================
Extended by other manifest providers.


BundleImportManifest
====================
Extended by other manifest providers.


Remote
======
A data channel for bundles to be pushed and pulled from. Extended by other apps to define remote types


PushRequest
===========
Extended by the remote, points to a bundle export


PullRequest
===========
Extended by the remote, points to a bundle import


=============
Purposed URLs
=============

/remote/ <- ParentModelResource
/remote/<remote type>/ <- ModelResource of the implemented remote
/remote/<remote type>/<id>/pull/add/ <- add pull request
/remote/<remote type>/<id>/pull/<id>/<manifest type>/add/ <- add manifest to pull (limit 1 per pull)

/bundle-export/ <- ParentModelResource
/bundle-export/<manifest type>/ <- ModelResource
/bundle-export/<manifest type>/add/ ; select data to export
/bundle-export/<manifest type>/<id>/push/<remote id>/add/ ; push to a remote, creates a push request
/bundle-export/<manifest type>/<id>/push/<remote id>/<push request id>/ ; view push request

Unapproved
==========

/bundle-import/ <- ParentModelResource
/bundle-import/<manifest type>/ <- ModelResource
/bundle-import/<manifest type>/add/ ; configures the import????

/push-request/ <- ParentModelResource
/push-request/<request type>/ <- ModelResource
/push-request/<request type>/add/ ; asks for a bundle export, asks for a configred remote corresponding to our type

/pull-request/ <- ParentModelResource
/pull-request/<request type>/ <- ModelResource
/pull-request/<request type>/add/ ; asks for a bundle import, asks for a configred remote corresponding to our type, ???


=========
Workflows
=========

Add remote
==========

# goto "/remote/"
# greeted with an add button for each remote type
# click on add, redirected to /remote/<remote type>/add/
# fill out remote

Send a push request
====================

# goto "/bundle-export/"
# greeted with an add button for each manifest type
# click on add, redirected to /bundle-export/<manifest type>/add/
# select data to export, save new manifest
# a link for each remote appears for pushing the bundle
# click on push to remote, redirected to /bundle-export/<manifest type>/<id>/push/<remote id>/add/

Receing a pull request
======================

# goto /remote/<remote type>/<id>/
# greeted with an add button for pull request
# click on add, redirected to /remote/<remote type>/<id>/pull/add/
# configure pull request, specifying the data source, save the request
# a link for each manifest type is presented to add a manifest to the pull request
# clink on link, redirected to /remote/<remote type>/<id>/pull/<id>/<manifest type>/add/
# fill out manifest loading options
! only one manifest is allowed per pull request
