from flask import Flask, Blueprint
from mdb.db import active_db
home_app = Blueprint('home', __name__, template_folder='templates/')
home_app.active_mdb = active_db

import mdb.home.views
