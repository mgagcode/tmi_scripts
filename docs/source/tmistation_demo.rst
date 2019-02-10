TMIStation Demo
###############

**TMIStation**

This is the program that production operators would use, interfaces with test equipment and the Device Under Test (DUT)

* The instructions are split into two catagories,

  * Basic

    * Simplest and fastest way to see `TMIStation`

  * Full

    * Uses `git` to clone a prescriptive directory structure used by `TMIStation`

Basic
*****

The Basic Demo is the easiest and fastest way to try out TMIStation.  However you will not be able to
edit or create new scripts.

Requirements
============

* Operating System

  * The system was developed on both Windows 10 and Ubuntu 18.04
  * Most testing occurs on Ubuntu given its the expected OS used in the factory because of cost (its free)
  * All these instructions are for Ubuntu 18.04

* Outside Software Requirements

  * Google Chrome browser (other browsers are not tested)
  * install Docker CE (https://docs.docker.com/install/linux/docker-ce/ubuntu/)


Installation
============

TMI programs are deployed as Docker containers, which allows the programs to run in a virtual
environment, and be independent of your host operating system.  This means, for example, that you don't have
to worry about python packages, versions of modules, etc

* Run **tmistation** container::

    docker run -ti -p 6800:6800 mgagcode/tmistation

  * Open Google Chrome to

    http://127.0.0.1:6800

* TMIStation login user/password is admin/admin
  * Other users passwords are `qwerty`
  * To **update** `tmistation` container use::

    docker pull mgagcode/tmistation

* Run your first script

  * Select pulldown menu item `Test Config`
  * Select script `prod_0.tmiscr`
  * Press button `Submit`
  * If everything checked out, the `Test` button will turn Green, press it, and you should be on the test screen, press Play to test
  * **Note:** The tests have delays in them for demo effect.  The delays are not needed.

Full
****

The Full Demo assume you have followed the instructions for the basic_ demo.

The Full Demo works by creating a local file structure and telling the ``tmistation`` Docker container to use that
local file system.  This requires a more advanced `docker run` command.

`Git <https://git-scm.com/>`_ and `Github <http://www.github.com>`_ are used.


Additional Requirements
=======================

* install git::

    sudo apt update
    sudo apt install git

  * if you are unfamiliar with `git`, in short it is a free cloud based software version control platform
  * `git` is an advanced tool, and although widely used, it can be an complicated tool.  There are
    GUI programs that try and make `git` easier for the novice user, and a quick google can point you to some for your host operating system.
  * TMI instructions (attempt to) only use the simple basic commands of `git`


Clone TMIScripts
================

* There is a prescriptive directory structure to use, and that is stored on `github` in a project called ``tmi_scripts``
* This `github` repo is where you would ultimately store and version control your own scripts

  * Instead of cloning the repo, you would *fork* [1]_ (copy) it, making it your own, and then add your own code
* The instructions below will create a folder called *git/tmistation* which `git` will copy the required files into

* Clone ``tmi_scripts``::

    mkdir ~/git
    mkdir ~/git/tmistation
    cd ~/git/tmistation
    git clone https://github.com/mgagcode/tmi_scripts.git

Run
===

* Run TMIStation::

    cd ~/git/tmistation/tmi_scripts/public
    docker run -ti -p 6800:6800 -v $(pwd):/app/public tmistation

* Open Google Chrome to

        http://127.0.0.1:6800


.. [1] This is covered in section TBD



