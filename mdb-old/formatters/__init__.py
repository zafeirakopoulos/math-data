import os
from flask import Flask, Blueprint
from mdb.data.init_db import *

mdb_path = os.getcwd()
mdb_definition = '{"paths": ["raw", "general", "options"]}'
mdb_name = "live"

data_app = Blueprint('data', __name__, template_folder='templates/data')
data_app.active_mdb = init_mdb(mdb_path, mdb_name, mdb_definition)

import mdb.data.views
