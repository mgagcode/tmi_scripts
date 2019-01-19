# TMI Station/Server Production Test System

* Now in **BETA**
* A framework to develop automated production test fixtures
* Single PC can control multiple test fixtures
* Write Python scripts to control measurement equipment and other fixtures
* APIs for recording measurements, setting Pass/Fail, locking resources, etc
* Server dashboard to monitor production yield, rate, etc
* Check out the [PDF](https://github.com/mgagcode/tmi_scripts/blob/master/TMISystem_Overview_06.pdf) slide deck for more information
* postgresql backend
* deployed as Docker containers for easy installation

# Screenshots
![TMIStation_1](app/test_view_4.png)

![TMIStation_1](app/tmiserver_1.png)

# Installation
* There are 3 components to the system
  * TMIStation
    * This is the interface that production operators would use
    * There can be many TMIStations on a LAN
  * TMIServer
    * There should only be one of these per LAN
    * Should have a fixed IP address
  * postgresql backend
    * There should only be one of these per LAN
    * Should have a fixed IP address
* Its possible that ONE PC can host all three components, and thats how these DEMO instructions are applied.
  * more distributed architectures are recommended for real production
  * ONE station is easier to DEMO because localhost is used for IP addresses
* Operating System
  * The system was developed on both Windows 10 and Ubuntu 18.04
  * Most testing occurs on Ubuntu given its the expected OS used in the factory because of cost (its free)
  * All these instructions are for Ubuntu
    * You should remove modemmanager as it seems to interfere with serial ports
    
      `sudo apt-get purge modemmanager`
      
    * see for granting Visa access to USB devices, https://stackoverflow.com/questions/52256123
      
* Outside Software Requirements (its all free)
  * Google Chrome browser (other browsers are not tested)
  * install Docker (https://docs.docker.com/install/linux/docker-ce/ubuntu/)
  * Python IDE (many to choose from) (NOT needed for the DEMO)
    * https://www.jetbrains.com/pycharm/download/#section=linux
  * git (NOT needed for pure DEMO mode)
  
    `sudo apt-get install git`
* TMIStation (pure DEMO mode)
  * Run "tmistation" container
  
    `docker run -ti -p 6800:6800 mgagcode/tmistation`

    * Open Google Chrome to
  
         http://127.0.0.1:6800 

    * TMIStation login user/password is admin/admin
    * To **update** tmistation use `docker pull mgagcode/tmistation` before running it.
    
  * Run your first script
    * Select pulldown menu item 'Test Config'
    * Select script 'prod_0.tmiscr'
    * Press button 'Submit'
    * If everything checked out, the 'Test' button will turn Green, press it, and you should be on the test screen, press Play to test
    * **Note:** The tests have delays in them for demo effect.  The delays are not needed.
* TMIServer (pure DEMO mode)
  * TMIServer needs the postgresql backend to be running in order to work
    * make a new directory in your home directory, change into it, create a data directory, and run Docker postgres command (this will pull postgres container)
    
        ```
        mkdir ~/postgres
        cd ~/postgres
        mkdir datadir
        docker run -p 5432:5432 -v $(pwd)/datadir:/var/lib/postgresql/data -e POSTGRES_PASSWORD=qwerty -d postgres:11
        ```
        * now create the required databases - you only need to do this **ONCE**
            ```
            docker exec -it tmi-postgres bash
            psql -U postgres
            CREATE DATABASE ResultBaseV1;
            CREATE DATABASE ResultBaseKeysV1;
            \q
            exit
            
    * The postgres container needs to be restarted every time you reboot your PC.  Or consider this,
    
        https://serverfault.com/questions/633067/how-do-i-auto-start-docker-containers-at-system-boot
    
  * Run "tmiserver" container
    
        `docker run -ti -p 6600:6600 mgagcode/tmiserver`

      * Open Google Chrome to
      
           http://127.0.0.1:6600 

    * TMIServer login user/password is admin/admin
    * To **update** tmiserver use `docker pull mgagcode/tmiserver` before running it.
    

* NON-PURE-DEMO mode
  * In Pure DEMO mode above, any files created by TMIStation/Server are stored in the container, and Docker containers do not
retain these files between runs (meaning you lose all your data), and you cannot access any files to change them.
  * In NON-PURE-DEMO mode, a local volume is mapped to the container, and TMIStation/Server will use that volume for files - which you will have access to. 
  * There is a prescriptive directory structure to use, and that is stored on github, so we will be cloning that (which is actually THIS) repo
    * This github repo is how you would version control your own scripts.  Instead of cloning the repo, you would fork it, making it your own, and then add your own code.
    * In this way, when TMI gets updated with new drivers and such, you can easily pull those to your fork as well
  * TMIStation
  
    ```
    mkdir ~/git
    mkdir ~/git/tmistation
    cd ~/git/tmistation
    git clone https://github.com/mgagcode/tmi_scripts.git
    cd ~/git/tmistation/tmi_scripts/public
    docker run -ti -p 6800:6800 -v $(pwd):/app/public tmistation
    ```
  
    * Open Google Chrome to
  
        http://127.0.0.1:6800 
        
  * TMIServer
  
    ```
    mkdir ~/git
    mkdir ~/git/tmiserver
    cd ~/git/tmiserver
    git clone https://github.com/mgagcode/tmi_scripts.git
    cd ~/git/tmiserver/tmi_scripts/public
    docker run -ti -p 6600:6600 -v $(pwd):/app/public mgagcode/tmiserver
    ```
  
    * Open Google Chrome to
  
        http://127.0.0.1:6600 

# TMI Scripts
* Examples of scripts/code
    * Testing is controlled by JSON 'script files'
      * Human readable, allows for non-programmers to change limits, enable/disable tests
    * Script files 
      * reference python code that runs the script
      * contain the arguments that drive the test
      * can have an `enable` field to enable/disable the test
* **Check out python script code `public/station/scripts/prod_v0/tsts00xx.py`**
  * This code demonstrates all of the API functions available to the programmer
  * Fun excersize
    * change the number of channels from 1 to 4, to show parallel channels running at the same time
    * The number of channels for the `prod_0.tmiscr` is determined by the "fake" HWDRV
    * Access `./public/stations/drivers/fake/tmi_fake.py` and change **NUM_CHANNELS** at the top of the file
* Check out the public directory
    * `./public/station/drivers`
      * examples of drivers, which configure the system
      * a script lists which drivers to load
      * see the Agilent scope driver, `./public/station/drivers/agilent_dso_usb_1/tmi_hwdrv_agilent_dso_usb_1.py`
      
# Development Installation
* A simple console environment is available for developing scripts outside of the web GUI interface
* Development on Ubuntu 18.04, or Windows 10
* Python 3.6+ is required
* Clone this repo to get started (its the same setup as the TMIStation, except we won't be running the TMIStation Docker image)

    ```
    mkdir ~/git
    mkdir ~/git/tmistation
    cd ~/git/tmistation
    git clone https://github.com/mgagcode/tmi_scripts.git
    cd ~/git/tmistation/tmi_scripts

* Run this command to test if everything is working,

    `python3 tmidev.py --script public/station/scripts/prod_v0/prod_0.tmiscr`
    
* The same source code that runs in the console, also runs in the web GUI.  Its much faster to develop code in the console, using your fav Python IDE.
    
# Contact
* email: `martin.guthrie.code@gmail.com`
