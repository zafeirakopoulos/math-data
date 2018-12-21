import os
import sys
import optparse
from flask import Flask, Blueprint, request, json

from db import *
# from rest.benchmarks import benchmarks_app

data_app = Blueprint('data_app', __name__, template_folder='templates')


@data_app.route('/instance/<key>',methods=['GET', 'POST'])
def instance(key):
    response = mdb.retrieve_data_from_database(key)
    return response


@data_app.route('/instances', methods=["GET"])
def instances():
    response = mdb.mdb_index()
    return ",".join([str(i) for i in response])

@data_app.route('/add_instance', methods=["POST"])
def add_instance(): # function already defined io.py
    content = request.json
    response = mdb.add_data_to_database(data)
    js = json.dumps()
    return js

@data_app.route('/shutdown', methods=["POST"])
def shutdown():
    request.environ.get('werkzeug.server.shutdown')()

name = "live"
########################
base_path=os.getcwd()
defition = {"paths": ["raw", "general", "options"]}
mdb = MathDataBase(base_path,name, defition)

data = '{"name": "Directed Edge and Vertex Weighted Graph", "raw": {"dense": {"edges": [[10, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 10, 0, 9, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 7, 0, 0], [0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 10, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 10, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 9, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 2, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]], "vertices": [5, 1, 5, 7, 9, 8, 7, 6, 9, 6, 8, 4, 3, 10, 4, 5, 2, 2, 10, 7]}}, "raw_types": {"dense": true, "sparse": false}, "attributes": {"edges": true, "vertices": true}, "plural": "Directed Edge and Vertex Weighted Graphs", "options": {"edges": {"directed": true, "weighted": true}, "vertices": {"weighted": true}}, "size": {"edges": 40, "vertices": 20}}'

data2 = '{"name": "Directed Edge and Vertex Weighted Graph", "raw": {"dewdew":55}, "options": {"dewetrue":3}, "size": {"edges": 40, "vertices": 20}}'

data_json = json.loads(data)
tree = mdb.add_data_to_database(data_json)
print(mdb.retrieve_data_from_database(tree))
ckey = mdb.approve_data(tree, "First one ever")
print(ckey)

data_json = json.loads(data2)
tree = mdb.add_data_to_database(data_json)
print(mdb.retrieve_data_from_database(tree))
ckey = mdb.approve_data(tree, "Second one ever")
print(ckey)
#######################

app = Flask(__name__)
app.register_blueprint(data_app, url_prefix='/data')
# app.register_blueprint(benchmarks_app, url_prefix='/benchmarks')
app.run()
