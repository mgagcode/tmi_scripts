Config
======

TMIServer configuration is done through a (modified) json file here,

::

    public/tmiserver.json

And its contents will be similar to,

::

    {
      "config": {
        # Should the result JSON files be stored as encrypted, true (default) or false,
        # If the results were not encrypted by TMIStation, they won't be ecrypted by TMIServer
        "results_bkup_encrypted": false
      },
      "postgres": {
        "ResultBaseKeysV1": {
          "user": "postgres",
          # !! Change "pw" to a real password for a real deployment
          # !! This pw must match your postgres deployment too
          "pw": "qwerty",
          "ip": "tmidb"
        }
      }
    }

This config file allows comments as lines with `#` as the first character.

`public/tmiserver.json` is **NOT** deployed to TMIStation by the TMIServer sync scripts management function.
TMIStation will only have the demo version of this file.

Two settings in this file you are likely to need to change at some point in the future,

* postgres:ResultBaseKeysV1:pw

  * needs to be changed to a secure value before deployment

* results_bkup_encrypted

  * You may or may not want TMIServer backups stored encrypted or not

    * encrypted, they are difficult to do anything with, for example if you wanted to add your own
      post porocessing, you could not do that with encrypted results

  * You may decide that the TMIServer at the top of the deployment, is in the cloud, and on this node it
    makes sense to store results as plain text, as presumably your cloud node is secure

