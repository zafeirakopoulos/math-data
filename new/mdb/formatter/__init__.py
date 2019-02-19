from flask import Flask, Blueprint
from mdb.db import active_db
formatter_app = Blueprint('formatter', __name__, template_folder='templates/formatter')
formatter_app.active_mdb = active_db

import mdb.formatter.views
