from flask import Flask, Blueprint
from mdb.data import data_app
from flask_bootstrap import Bootstrap

app = Flask("mdb")
Bootstrap(app)

app.config['EXPLAIN_TEMPLATE_LOADING'] = True
print("Correct app")
app.register_blueprint(data_app, url_prefix="/data")
