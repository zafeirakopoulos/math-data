import os
import subprocess

from mdb.backend.data import *
from mdb.backend.mdl import *


# Import the definition of the mathdata server
from mdb.md_def import *
from mdb.mdl_def import *

subprocess.run(["git","config","--global","user.email","admin@mdb.io"])
subprocess.run(["git","config","--global","user.name","MathaData Admin"])

active_db = init_mdb(mdb_path, mdb_name, mdb_definition)
active_mdl = MathDataLanguage(active_db)
