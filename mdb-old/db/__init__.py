import os
from mdb.db.init_db import *

mdb_path = os.getcwd()
mdb_definition = '{"paths": ["raw", "general", "options"]}'
mdb_name = "live"

active_db = init_mdb(mdb_path, mdb_name, mdb_definition)
