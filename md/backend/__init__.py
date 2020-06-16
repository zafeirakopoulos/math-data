import os
import subprocess

from md.backend.data import *
from md.backend.benchmarks import *

from md.backend.mdl import *


# Import the definition of the mathdata server
from md.md_def import *

subprocess.run(["git","config","--global","user.email","admin@mdb.io"])
subprocess.run(["git","config","--global","user.name","MathaData Admin"])

active_db = init_mdb(md_path, mdbase_name, mdbase_definition)
active_bench = init_bench(md_path, mdbench_name, mdbench_definition)

active_mdl = MathDataLanguage(active_db)
