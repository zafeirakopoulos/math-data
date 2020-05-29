from flask import Flask, Blueprint
from flask_security import login_required
from mdb.backend import active_db
from mdb.backend import active_mdl

data_app = Blueprint('data', __name__)
data_app.active_mdb = active_db
data_app.active_mdl = active_mdl
 

import mdb.views.data.views
