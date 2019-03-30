Development
###########

This section describes how to get started with your own development.

.. contents::
   :local:


Your Own Git Repo
*****************

You will want to begin with setting up your own Git repo.  If you are unfamiliar with Git,
then you should read up on it, and/or do some tutorials.  It is beyond the scope
of this documentation to teach Git.

To get started, create yourself a guthub account.

There are two ways to being using TMI with Git,

The first way, is to fork the `tmi_scripts` repo to your own github repo.  This is the
easiest way to get started, but it has the draw back that all git forks must be
public, and its very unlikley that you want that.  So the forking method will not be used
below, but you may use it if you want.

The second way is to clone tmi_scripts and push it to your own repo.  Detailed instructions
are shown below

* Create a new repository at github.com. (this is **your** repository)

  * Give it the same name as TMI repository, `tmi_scripts`
  * Don't initialize it with a README, .gitignore, or license.

* Clone the `tmi_scripts` repository repository to your local machine. (if you haven't done so already)

::

        git clone https://github.com/mgagcode/tmi_scripts.git

* Note that the `tmi_scripts` clone will be created under your current directory.
  Some prefer all their repositories to be under a common directory, so you might actually
  do something like this,

::

        mkdir ~/git
        cd ~/git
        git clone https://github.com/mgagcode/tmi_scripts.git

* Rename the local repository's current 'origin' to 'upstream'

::

        git remote rename origin upstream

* Give the local repository an 'origin' that points to your repository

::

        git remote add origin https://github.com/your-account/tmi_scripts.git

* Push the local repository to your repository on github

::

        git push origin master

* Now 'origin' points to your repository & 'upstream' points to the other repository

* Create a new branch for your changes with

::

        git checkout -b my-feature-branch

* You can git commit as usual to your repository

* To pull changes from TMI `tmi_scripts` to your master branch use,

::

        git pull upstream master

* You want to be able to pull from TMI `tmi_scripts` occasionally to get TMI updates to scripts, and/or
  examples, drivers, etc.

