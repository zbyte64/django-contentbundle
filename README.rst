TODO, this is ALPHA

The following are development notes.

======
Models
======

BundleExportManifest
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


BundleImportManifest
====================
Extended by other manifest providers.
Points to a pull request (one to one field)


=============
Purposed URLs
=============

* /remote/ <- ParentModelResource
* /remote/<remote type>/ <- ModelResource of the implemented remote
* /remote/<remote type>/<id>/pull/ <- PullRequestResource
* /remote/<remote type>/<id>/pull/add/ <- add pull request, fill out data source
* /remote/<remote type>/<id>/pull/<id>/<manifest type>/ <- Manifest resource (CRUD)?
* /remote/<remote type>/<id>/pull/<id>/<manifest type>/add/ <- add manifest to pull (limit 1 per pull), configure pull settings
* /remote/<remote type>/<id>/pull/<id>/<manifest type>/<mid>/ ;  view manifest, edit options
* /remote/<remote type>/<id>/pull/<id>/<manifest type>/<mid>/apply/ ; accept changes, merge


* /bundle-export/ <- ParentModelResource
* /bundle-export/<manifest type>/ <- ModelResource
* /bundle-export/<manifest type>/add/ ; select data to export
* /bundle-export/<manifest type>/<id>/push/ <- PushRequestResource
* /bundle-export/<manifest type>/<id>/push/add/<remote id>/ ; push to a remote, creates a push request
* /bundle-export/<manifest type>/<id>/push/<push request id>/ ; view push request

CONSIDER: hyperadmin should have a clear parent-child resource item design pattern.

=========
Workflows
=========

Add remote
==========

* goto "/remote/"
* greeted with an add button for each remote type
* click on add, redirected to /remote/<remote type>/add/
* fill out remote

Send a push request
====================

* goto "/bundle-export/"
* greeted with an add button for each manifest type
* click on add, redirected to /bundle-export/<manifest type>/add/
* select data to export, save new manifest
* a link for each remote appears for pushing the bundle
* click on push to remote, redirected to /bundle-export/<manifest type>/<id>/push/<remote id>/add/

Receing a pull request
======================

* goto /remote/<remote type>/<id>/
* greeted with an add button for pull request
* click on add, redirected to /remote/<remote type>/<id>/pull/add/
* configure pull request, specifying the data source, save the request
* a link for each manifest type is presented to add a manifest to the pull request
* clink on link, redirected to /remote/<remote type>/<id>/pull/<id>/<manifest type>/add/
* fill out manifest loading options

! only one manifest is allowed per pull request

