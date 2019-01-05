# TMI Station/Server Production Test System

* A framework to develop automated production test fixtures
* Single PC can control multiple test fixtures
* Write Python scripts to control measurement equipment and other fixtures
* APIs for recording measurements, setting Pass/Fail, locking resources, etc
* Server dashboard to monitor production yield, rate, etc
* Check out the PDF slide deck for more information

# TMI Scripts
* Examples of scripts/code
    * Testing is controlled by JSON 'script files'
      * Human readable, allows for non-programmers to change limits, enable/disable tests
    * Script files reference python code that runs the script
* Check out the public directory
    * other directories provide a framework for running code outside the framework, for development purposes

# Installation
* Development on Ubuntu 18.04, or Windows 10
* Python 3.6+
* Run this command to test if everything is working,

    `python3 tmidev.py --script public/station/scripts/prod_v0/prod_0.tmiscr`
    
# Advanced Notes
* Record Types
    * A record type defines the result JSON file and the backend server database
    * ResultBaseKeysV1
        * An example of how to extend the base record type
        * This extension is used for the Demo scripts
        * It extends the base class be adding 4 "keys" to the JSON result which end up as entries in the backend DB
        * Extending the base record type requires backend programming, don't extend the record type unless you have contacted TMI for backend support


## Add New Scripts 
1) Directory structure Considerations
   * Follow the demo scripts which are organized in directory tree
     * public
       * RecordType
         * Product

2) The filename of scripts and python code should include a version
3) Test items should also be versioned, see the example scripts

## Offline Development
1) An offline python script can be used to develop scripts outside of the GUI environment.

    `python tmidev.py --script <path_to_script>`

2) This will run your script to the console.
3) All the APIs available in the GUI are also available here.
4) The JSON result file will be produced.
