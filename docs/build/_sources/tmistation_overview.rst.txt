Overview
########

This is an overview of how TMIStation is structured.

Scripts and Programs
********************

TMIStation tests are driven by two things, ``scripts`` and ``programs``.

``Scripts``

* define the test sequence and operating modes of the test being run
* are in human readable JSON file format

  * JSON is used so that non-programmers may be able to read/edit [1]_ the script without requiring a
    programming background.  This is useful in development or emergency situations.

* extend JSON a little bit, by allowing comments, any line begining with `#` is a comment.  This allows
  the script to be documented

``Programs``

* written in Python (3.6)

Scripts
=======

``Scripts`` are a JSON file and are what is used to drive a test.  The ``script`` has the following sections,

::

    {
      "subs": {
      },
      "info": {
      },
      "config": {
      },
      "tests": [
      ]
    }


subs
----

This is a section of User configurable substitutions for variables in the script.  For example, if there was a test
limit that could have two values, the values can be listed as a `subs` field and the user can select which one to use.

Obviously, in a production environment, typically operators are not allowed to arbitrarily change values of test
limits or any other setup.  However, in an engineering lab, or new product ramp environment, having an easy method
to change some parameters might be useful.  This feature does not have to be used.

`subs` are also useful for generating :ref:`Travellers`.

Here is a full example of what `subs` section could look like,

::

  "subs": {
    # Each item here is described by,
    # "key":
    #   "title": "<title>",
    #   "type" : "<str|num>", "widget": "<textinput|select>",
    #   "regex": <"regex"|null|omit>, "default": <default>
    #
    # Rules:
    # 1. key must not have any spaces or special characters
    # 2. regex can be omitted if not applicable
    #
    "Lot": {
      "title": "Lot (format #####)",
      "type" : "str", "widget": "textinput", "regex": "^\\d{5}$", "default": "95035"
    },
    "Loc": {
      "title": "Location",
      "type" : "str", "widget": "select", "choices": ["canada/ontario/milton", "us/newyork/bufalo"]
    },
    "TST000Max": {
      "title": "TST000 Max Attenuation (db)",
      "type" : "num", "widget": "select", "choices": [9, 10, 11]
    }
  },

``key``

* the name of the variable to be replaced somewhere else in the script, for example, the variable could be in
  the ``info`` section

  * the variable in other sections, would be named ``"%%key"``
  * the variable would be listed with double quotes, regardless of the variable type
* ``key`` should not have any special characters in it, else bad things happen

``title``

* this is the title of the field to be presented to the Operator in the Test Config view
* if there is a specific format of the variable expected, that should be indicated in the ``title``

``type``

* indicates type of variable that is ultimately required in the final JSON version of the script
* string (`str`) and number (`num`) (covers float and ints) are the only options

``widget``

* the type of GUI widget to present to the Operator in the Test Config view
* `textinput` is a generic text input box, which will be populated by the ``default`` field
* `select` is a drop down selection menu

``regex``

* used only for `textinput` ``widget``
* used to validate the Operator entered correct information
* this is optional field

``default``

* sets the default value for `textinput` ``widget``

info
----

This section is a list of fields that correspond to fields that exist in the backend database and are typically
used for database searches.

You cannot add or delete fields from this section.  If there are missing fields, an error will occur downstream as the
result record is check to have these fields.  New fields can be added, but that requires a request to customize
the backend database.  See TBD.

Note that the example here, two fields are using the `subs` section to get their values from the Operator
in the Test Config view.

::

  "info": {
    "product": "widget_1",
    "bom": "B00012-001",
    # list fields present user choice or fill in
    "lot": "%%Lot",
    "location": "%%Loc"
  },

``product``, ``bom``, ``lot``, ``location`` are fields that you define a meaning specific to your operation.

Defining rules and a naming convention for these fields will help you later when you need to make database searches
for specific sets of results.  This is important.

config
------

tests
-----


.. [1] ``Scripts`` CAN BE LOCKED DOWN so that a production user cannot change them.  Locking down the TMIStation is covered TBD.
