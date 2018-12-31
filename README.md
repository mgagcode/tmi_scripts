# TMI Scripts

* Record Types
    * A record type defines the result JSON file and the backend server database
    * TMIDemoRecordV1
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
