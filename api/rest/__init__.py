import os
import sys
# sys.path.insert hack is necessary if we want to access mdb from api.
# I think putting api inside our business logic is uglier.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import optparse
from flask import Flask
# from mdb.rest.data import *
# from mdb.rest.benchmarks import *

from rest.data import data_app
from rest.benchmarks import benchmarks_app

app = Flask(__name__)
app.register_blueprint(data_app, url_prefix='/data')
app.register_blueprint(benchmarks_app, url_prefix='/benchmarks')


# The app should start in a separate thread
# This does not work in debug mode.
#thread.start_new_thread(flaskThread,())
