from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap

from mdb.data import data_app
from mdb.formatter import formatter_app

app = Flask("mdb")
Bootstrap(app)

app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.register_blueprint(data_app, url_prefix="/data")
app.register_blueprint(formatter_app, url_prefix="/formatter")
