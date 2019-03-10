import os
import subprocess

# Import the definition of the mathdata server
from mdb.md_def import *

from mdb.views.db.init_db import *


subprocess.run(["git","config","--global","user.email","admin@mdb.io"])
subprocess.run(["git","config","--global","user.name","MathaData Admin"])




active_db = init_mdb(mdb_path, mdb_name, mdb_definition)
