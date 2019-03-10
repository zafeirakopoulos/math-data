from flask import Flask, Blueprint
from flask_security import login_required
from mdb.views.db import active_db

data_app = Blueprint('data', __name__)
data_app.active_mdb = active_db

@data_app.before_request
@login_required
def before_request():
    pass

import mdb.views.data.views
