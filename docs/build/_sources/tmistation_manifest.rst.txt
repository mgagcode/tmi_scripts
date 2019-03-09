Manifest
########

A method by which your scripts and programs are protected from changes (hacks) in the production environment.

TMIStation will not operate if the Manifest is not validated.

The manifest is an encrypted file at this location,

::

    public/station/manifest.tmi

This file holds a list of files from `pubic/station` along with a hash of each file, which is used
by TMIStation to check if any changes have been made to any of the files.  If a file has been changed,
TMIStation will not operate.

To enable manifest checking, the `tmistation.json` file must have this setting,

::

    "manifest_locked": true,


If `manifest_locked` is `false`, which it is in demo and development scenarios, ONLY the `tmistation.json` itself is
in the manifest.  Therefore, `tmistation.json` file can never be changed without updating the manifest file.


Exclusions
**********

When `manifest_locked` is `true` every file in the `pubic/station` path is added to the manifest, and therefore
becomes locked.  Any changes, TMIStation will not operate.

In the case that you have files that change content during testing, you may exclude those files by listing them
in,

::

    public/station/manifest.exc



Update Manifest
***************

TMIServer can update the manifest.  See main drop down menu, Station Management.

In a deployed production environment, TMIServer deploys scripts/programs to the attached TMIStations. This
process includes a update of the Manifest.
