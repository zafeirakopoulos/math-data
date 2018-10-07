#!/bin/sh
sphinx-apidoc -f -o doc/source/ mdb/
sphinx-apidoc -f -o doc/source/ service/
cd doc 
make html
make latexpdf
cd ..