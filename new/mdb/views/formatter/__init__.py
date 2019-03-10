from flask import Flask, Blueprint
from mdb.views.db import active_db

formatter_app = Blueprint('formatter', __name__)
formatter_app.active_mdb = active_db

import mdb.views.formatter.views
