"""
Output:
Python 3.7.7 (default, Mar 27 2020, 00:18:04) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from index_database import IndexDatabase
>>> idb = IndexDatabase("mdbase", initialize=True)
>>> idb.sql_add_commit("a0asdadx1", 0)
>>> idb.sql_get_address_from_commit("a0asdadx1")
'mdbase.git'
>>> 
>>> idb.sql_add_repository("mdbase2.git")
>>> idb.sql_get_repository_address(1)
'mdbase2.git'
>>> 
>>> idb.sql_set_repository_address(1, "https://md.com/mdbase3.git")
>>> idb.sql_get_repository_address(1)
'https://md.com/mdbase3.git'
>>> 
>>> idb.sql_remove_commit("a0asdadx1")
>>> try:
...     idb.sql_get_address_from_commit("a0asdadx1")
... except Exception as e:
...     if "No commit" in str(e):
...             print("Successfully removed commit")
... 
Successfully removed commit
>>> idb.sql_get_last_repository_id()
1
>>> 
"""



from md.backend.repository_database import IndexDatabase
idb = IndexDatabase("mdbase", initialize=True)
idb.sql_add_commit("a0asdadx1", 0)
idb.sql_get_address_from_commit("a0asdadx1")

idb.sql_add_repository("mdbase2.git")
idb.sql_get_repository_address(1)

idb.sql_set_repository_address(1, "https://md.com/mdbase3.git")
idb.sql_get_repository_address(1)

idb.sql_remove_commit("a0asdadx1")
try:
	idb.sql_get_address_from_commit("a0asdadx1")
except Exception as e:
	if "No commit" in str(e):
		print("Successfully removed commit")

idb.sql_get_last_repository_id()
