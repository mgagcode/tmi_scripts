Security
########

Production security is important.  TMI has some features and suggestions to improve security.

.. contents::
   :local:


TMIServer
=========

It is assumed that TMIServers are "physically secure", which means physical access to the computers is
restricted in some way, for example, locked in a secure room.

The following are further suggestions to improve security,

* encrypt the hard disk by the OS
* strong admin password
* use TMI Account Roles for users


TMIStation
==========

TMIStations are considered insecure.  Presumably anyone on the production floor can access a TMIStation.
Often login names and passwords are common to a group of people, or shared amoung them to access the computer.

The following are further suggestions to improve security,

* encrypt the hard disk by the OS
* strong admin password
* enable TMI Manifest locking, see :ref:`tmistation_manifest:Manifest`
* enable result encryption
* regularly purge the backups from the disk, (or disable backups, not recommended)
* use TMI Account Roles for users


Postgres DB
===========

* Change the default password!

  * See the pstgres starter script `public\tmipostg.sh --help`
  * Also remember to use the same password in the TMIServer config json, `public\tmiserver.json`
  * `public\tmiserver.json` is not deployed to TMIStations by TMIServer
