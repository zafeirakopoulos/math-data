from flask import Flask, Blueprint
from mdb.db import active_db
data_app = Blueprint('data', __name__, template_folder='templates/')
data_app.active_mdb = active_db

import mdb.data.views
