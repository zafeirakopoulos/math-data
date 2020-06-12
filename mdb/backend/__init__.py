import os
import subprocess

from md.backend.data import *
from md.backend.mdl import *


# Import the definition of the mathdata server
from md.md_def import *
from md.mdl_def import *

subprocess.run(["git","config","--global","user.email","admin@mdb.io"])
subprocess.run(["git","config","--global","user.name","MathaData Admin"])

active_db = init_mdb(mdb_path, mdb_name, mdb_definition)
active_mdl = MathDataLanguage(active_db)
