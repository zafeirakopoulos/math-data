from flask import Flask, Blueprint
from mdb.backend.db import active_db

home_app = Blueprint('home', __name__)
home_app.active_mdb = active_db

import mdb.views.home.views
