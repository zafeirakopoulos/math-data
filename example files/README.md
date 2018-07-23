# Example Files

These are some simple example files to report the current state of the project. Files and their explanation will be updated as needed.

## dataset.json

This is an example for static data-set file. 
* `data` field contains the data that will be fed into the input parser for the program.
* `formats` represents the possible formats that the data field satisfies
* `features` represents the special features(that does not fit as format specifier), like _value range_
  
## generator.json

This is an example for generator based data-set file.
* `generator` field represents the properties of the generator type data-set.
* `generator.deterministic` tells if the generated data is deterministic or not.
* `generator.executable` represents the target executable. If the executable path starts with a `./`(dot) it will be searched in the benchmark files, otherwise operating system predefined paths will be used.

## gen.py

Simple random number generating script to demonstrate the generator.