Basic Demo
==========

There are 3 components to the system

* **TMIStation**

  * This is the program that production operators would use, interfaces with test equipment and the Device Under Test

* **TMIServer**

  * This provides summary dashboards and backend database

* postgresql backend

  * There should only be one of these per LAN

It is possible that ONE PC can host all three components, and that is how these DEMO instructions are applied

* more distributed architectures are recommended for real production
* ONE computer is just easier for a demo
* You do not need any special equipment to run the demo.  There is a demo script that interfaces to nothing external and shows many of the user interface features.


Requirements
------------

* Operating System

  * The system was developed on both Windows 10 and Ubuntu 18.04
  * Most testing occurs on Ubuntu given its the expected OS used in the factory because of cost (its free)
  * All these instructions are for Ubuntu 18.04

* Outside Software Requirements

  * Google Chrome browser (other browsers are not tested)
  * install Docker CE (https://docs.docker.com/install/linux/docker-ce/ubuntu/)


Installation
------------

TMI programs are deployed as Docker containers, which allows the programs to run in a virtual
environment, and be independent of your host operating system.  This means, for example, that you don't have
to worry about python packages, versions of modules, etc

The easiest demo to load and play with is the TMIStation demo.

TMIStation
^^^^^^^^^^

  * Run **tmistation** container::

        docker run -ti -p 6800:6800 mgagcode/tmistation

    * Open Google Chrome to

         http://127.0.0.1:6800

    * TMIStation login user/password is admin/admin
    * Other users passwords are `qwerty`
    * To **update** tmistation use::

        docker pull mgagcode/tmistation

  * Run your first script

    * Select pulldown menu item `Test Config`
    * Select script `prod_0.tmiscr`
    * Press button `Submit`
    * If everything checked out, the `Test` button will turn Green, press it, and you should be on the test screen, press Play to test
    * **Note:** The tests have delays in them for demo effect.  The delays are not needed.
