from flask import Flask, Blueprint
from flask_security import login_required
from md.backend import active_db, active_mdl

mdl_app = Blueprint('mdl', __name__)
mdl_app.active_mdb = active_db
mdl_app.active_mdl = active_mdl

import md.views.mdl.views
