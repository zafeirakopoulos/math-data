from flask import Flask, Blueprint, request, json
import os
import mdb
from mdb.data.db import DB
from mdb.data.io import *
from mdb.data.setup import *


mdb_data = mdb.data.setup.__mdb

data_app = Blueprint('data_app', __name__, template_folder='templates')

# @data_app.route('/', defaults={'page': 'index'})
# def index(page):
#     try:
#         return render_template('pages/%s.html' % page)
#     except TemplateNotFound:
#         abort(404)


@data_app.route('/add_instance', methods=["POST"])
def add_instance():

    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)

    instance = request.json

    response = mdb.io.add_instance(data, instance)

    js = json.dumps(response)

    return js


@data_app.route('/filter', methods=["POST"])
def filter():

    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)

    instance = request.json

    # filter method are not written yet
    response = search.filter(data, instance)

    js = json.dumps(response)

    return js
@data_app.route('/dataset', methods=["POST"])
def dataset():
    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)
    instance = request.json
    # dataset method are not written yet
    response = search.search(data, instance)
    js = json.dumps(response)
    return js

@data_app.route('/datatypes', methods=["GET"])
def datatypes():
    # it is an example
    data = [
        {"datatype": "graph"},
        {"datatype": "polynomial"},
        {"datatype": "list"}
    ]
    js = json.dumps(data)
    return js

@data_app.route('/datasets', methods=["GET"])
def datasets():

    # it is an example
    data = [
        {"vertex": "20"},
        {"edge": "10"},
    ]

    js = json.dumps(data)

    return js


@data_app.route('/instances', methods=["GET"])
def instances():

    # it is an example
    instance = [
        {
            "raw": "something-",
            "features": "something-",
            "semantics": "something-",
            "context": {"edge": {"1": 99, "2": 3},
                        "vertex": [{"first": 1, "second": 2},
                                   {"first": 2, "second": 3}]},
            "typeset": "something-",
            "commit": "commit-message"
        },

        {
            "raw": "1",
            "features": "2-",
            "semantics": "2-",
            "context": {"edge": {"1": 99, "2": 3},
                        "vertex": [{"first": 1, "second": 2},
                                   {"first": 2, "second": 3}]},
            "typeset": "3-",
            "commit": "commit-message"
        }
    ]

    js = json.dumps(instance)

    return js


@data_app.route('/instance', methods=["POST"])
def instance():

    # it is an example

    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)
    instance = request.json

    response = io.retrieve_instance(data, instance)

    js = json.dumps(response)

    return js

@data_app.route('/shutdown', methods=["POST"])
def shutdown():
    flask.request.environ.get('werkzeug.server.shutdown')()
