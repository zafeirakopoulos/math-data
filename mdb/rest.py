from flask import Flask,request, json
import os
from mdb.db import DB
from mdb.io import *


app = Flask(__name__)

@app.route('/add_instance', methods=["POST"])
def add_instance():

    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)

    instance = request.json

    response = mdb.io.add_instance(data, instance)

    js = json.dumps(response)

    return js


@app.route('/filter', methods=["POST"])
def filter():

    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)

    instance = request.json

    # filter method are not written yet
    response = search.filter(data, instance)

    js = json.dumps(response)

    return js
@app.route('/dataset', methods=["POST"])
def dataset():
    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)
    instance = request.json
    # dataset method are not written yet
    response = search.search(data, instance)
    js = json.dumps(response)
    return js

@app.route('/datatypes', methods=["GET"])
def datatypes():
    # it is an example
    data = [
        {"datatype": "graph"},
        {"datatype": "polynomial"},
        {"datatype": "list"}
    ]
    js = json.dumps(data)
    return js

@app.route('/datasets', methods=["GET"])
def datasets():

    # it is an example
    data = [
        {"vertex": "20"},
        {"edge": "10"},
    ]

    js = json.dumps(data)

    return js


@app.route('/instances', methods=["GET"])
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


@app.route('/instance', methods=["POST"])
def instance():

    # it is an example

    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)
    instance = request.json

    response = io.retrieve_instance(data, instance)

    js = json.dumps(response)

    return js

if __name__ == '__main__':
   print(sys.argv[0])
   app.run(debug=True)
