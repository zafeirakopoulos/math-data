from flask import Flask
from rest.data import *
from rest.benchmarks import *

app = Flask(__name__)
app.register_blueprint(data_app, url_prefix='/data')
app.register_blueprint(benchmarks_app, url_prefix='/benchmarks')

# The app should start in a separate thread 
# This does not work in debug mode.
#thread.start_new_thread(flaskThread,())
