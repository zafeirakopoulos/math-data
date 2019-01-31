from flask import Flask, Blueprint, request, json, render_template
from mdb.data import data_app

@data_app.route('/',methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@data_app.route('/instance/<key>',methods=['GET', 'POST'])
def instance(key):
    response = data_app.active_mdb.retrieve_data_from_database(key)
    return response


@data_app.route('/instances', methods=["GET"])
def instances():
    print("instances requested")

    response = data_app.active_mdb.mdb_index()
    return json.dumps(response)

@data_app.route('/add_instance', methods=["POST"])
def add_instance(): # function already defined io.py
    content = request.json
    response = data_app.active_mdb.add_data_to_database(data)
    js = json.dumps()
    return js

@data_app.route('/shutdown', methods=["POST"])
def shutdown():
    request.environ.get('werkzeug.server.shutdown')()
