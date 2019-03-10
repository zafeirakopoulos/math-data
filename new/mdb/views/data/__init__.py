from flask import Flask, Blueprint
from mdb.views.db import active_db

data_app = Blueprint('data', __name__)
data_app.active_mdb = active_db

import mdb.views.data.views
