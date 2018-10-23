#!/bin/sh
sphinx-apidoc -f -o source/ mdb/
sphinx-apidoc -f -o source/ mdb/data/app/
cd doc
make html
make latex
cd build/latex/
pdflatex MathDataBench.tex
cd ../../..