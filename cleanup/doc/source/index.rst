.. MathDataBench documentation master file, created by
   sphinx-quickstart on Sun Oct  7 12:11:23 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MathDataBench's documentation!
=========================================
The MD-project has 3 main components:

* MD-language
* MD-Library
* RESTful API and JupyterLab extension


Goal
----
The goal of the project is to have a system for storing, retrieving and searching MD in a consistent and robust way.
This system can be used either locally by the user or online as a service.
For the local version, a JupyterLab is provided. Since JupterLab is a standard tool in data science, the intension is to incorporate MD in the standard data science workflow.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
Services
========
Following sections contain docstring of each service
 
1.Software Service
------------------
	.. automodule:: service.software
		:members:

2.Users Service
---------------
	.. automodule:: service.users
		:members:

3.Format Service
----------------
	.. automodule:: service.format
		:members:

4.Environment Service
----------------
	.. automodule:: service.environment
		:members:

5.Bibliography Service
----------------
	.. automodule:: service.bibliography
		:members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
