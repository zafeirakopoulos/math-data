from flask import Flask, Blueprint, request, json, render_template, jsonify
from flask_login import current_user
from mdb.views.data import data_app
from mdb.core import logger

import sys

import json as json_beautifier

##########################
##########################
##   API
##########################
##########################
@data_app.route('api/instance/<key>',methods=['GET', 'POST'])
def api_instance(key):
    return data_app.active_mdb.retrieve_instance_from_database(key)

@data_app.route('api/instances', methods=["GET"])
def api_instances():
    return "["+",".join(data_app.active_mdb.get_instances())+"]"

@data_app.route('api/definition/<key>',methods=['GET', 'POST'])
def api_definition(key):
    return data_app.active_mdb.retrieve_definition(key)

@data_app.route('api/definitions', methods=["GET"])
def api_definitions():
    return data_app.active_mdb.definition_index()

def pp_json(json_thing, sort=False, indents=4):
    parsed_json = json_beautifier.loads(json_thing)
    return json_beautifier.dumps(parsed_json, indent = indents, sort_keys=sort)


##########################
##########################
##   HTML
##########################
##########################
@data_app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("data/index.html")


@data_app.route('/browse', methods=['GET', 'POST'])
def browse():
    return render_template("data/browse.html")


@data_app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template("data/create.html")

@data_app.route('/edit', methods=['GET', 'POST'])
def edit():
    return render_template("data/edit.html")

# retrieves an instance object
@data_app.route('/instance/<key>', methods=['GET', 'POST'])
def instance(key):
    response = data_app.active_mdb.retrieve_instance(key)
    # get actual json from json_dumps
    instance_data = json_beautifier.loads(response)


    out = {}

    # get html representation for instance object and add to output
    out["page"] = render_template("data/instance.html", instance=json_beautifier.dumps(instance_data, indent = 4, sort_keys=False), key=key)

    instance_data["formatters"]= data_app.active_mdb.retrieve_formatter_for(instance_data["datastructure"])

    # add actual json to output
    out["data"] = instance_data

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

# function to list all instances
@data_app.route('/instances', methods=["GET"])
def instances():
    #  A dictionary of key-name pairs
    instances = {}
    for key in data_app.active_mdb.get_instances():
        instances[key]= json_beautifier.loads(data_app.active_mdb.retrieve_instance(key))["name"]

    return render_template("data/instances.html", instances=instances)

# function to retrieve a datastructure
@data_app.route('/datastructure/<key>', methods=['GET', 'POST'])
def datastructure(key):
    response = data_app.active_mdb.retrieve_datastructure(key)
    json_data = json_beautifier.loads(response)

    out = {}

    # get html representation for defnition object and add to output
    out["page"] = render_template("data/datastructure.html", datastructure=json_beautifier.dumps(json_data, indent = 4, sort_keys=False), key=key)

    # add actual json to output
    out["data"] = json_data

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

@data_app.route('/datastructures/<action>', methods=["GET"])
def datastructures(action):
    if action=="create_instance":
        action="register"
    if action=="browse_datastructures":
        action="show"

    #  A dictionary of key-name pairs
    datastructures = {}
    for key in data_app.active_mdb.get_datastructures():
        datastructures[key]= json_beautifier.loads(data_app.active_mdb.retrieve_datastructure(key))["name"]

    return render_template("data/datastructures.html", datastructures=datastructures, action=action)

##############################################################################
########################## Datasets  #########################################
##############################################################################


# function to retrieve a datastructure
@data_app.route('/dataset/<key>', methods=['GET', 'POST'])
def dataset(key):
    response = data_app.active_mdb.retrieve_dataset(key)
    json_data = json_beautifier.loads(response)

    out = {}

    # get html representation for defnition object and add to output
    out["page"] = render_template("data/dataset.html", dataset=json_beautifier.dumps(json_data, indent = 4, sort_keys=False), key=key)

    # add actual json to output
    out["data"] = json_data

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

@data_app.route('/datasets/<action>', methods=["GET"])
def datasets(action):
    if action=="create_instance":
        action="register"
    if action=="browse_datastructures":
        action="show"

    #  A dictionary of key-name pairs
    datasets = {}
    for key in data_app.active_mdb.get_datasets():
        datasets[key]= json_beautifier.loads(data_app.active_mdb.retrieve_dataset(key))["name"]

    return render_template("data/datasets.html", datastructures=datasets, action=action)

##############################################################################
##############################################################################
##############################################################################

@data_app.route('/add_instance', methods=["POST"])
def add_instance():
    body = request.form['body']
    body = body[1:-1]

    message = "Instance created by " + current_user.email

    response = data_app.active_mdb.add_instance(body, message)
    logger.debug("response: " + str(response))

    return response

@data_app.route('/add_datastructure', methods=["POST"])
def add_datastructure():
    body = request.form['body']
    body = body[1:-1]

    message = "Datastructure created by " + current_user.email

    response = data_app.active_mdb.add_datastructure(body, message)
    logger.debug("response: " + str(response))

    return response

@data_app.route('/add_instance_data_field', methods=["GET"])
def add_instance_data_field():
    return render_template("data/data_field_add_instance.html")


# this method is called when the edit button is clicked for instances
# input is the edited instance object
@data_app.route('/edit_instance', methods=["POST"])
def edit_instance():
    # TODO: fill this function to actually send edit request to backend
    body = request.form['body']
    body = body[1:-1]
    key = request.form['instanceKey']

    #logger.debug("body: " + body)

    message = "Instance changed by " + current_user.email + " old key: " + str(key)

    response = data_app.active_mdb.add_instance(body, message)
    #logger.debug("response: " + str(response))

    return response


# this method is called when the edit button is clicked for datastructures.
# input is the edited datastructure object
@data_app.route('/edit_datastructure', methods=["POST"])
def edit_datastructure():
    body = request.form['body']
    body = body[1:-1]
    datastructureKey = request.form['datastructureKey']

    #logger.debug("body: " + body)

    message = "Datastructure changed by " + current_user.email + " old key: " + str(datastructureKey)

    response = data_app.active_mdb.add_datastructure(body, message)
    #logger.debug("response: " + str(response))

    return response

def remove_at(i, s):
    return s[:i] + s[i+1:]

# function to get change list
@data_app.route('/editor', methods=["GET", "POST"])
def editor_page():
    pending_ds = data_app.active_mdb.pending_datastructures()
    pending_ins = data_app.active_mdb.pending_instances()

    return render_template("data/editor.html", datastructures=pending_ds, instances=pending_ins)

# method that gets a change's details by id
@data_app.route('/change/<change_id>/<data_type>', methods=['GET'])
def get_change(change_id, data_type):
    response = data_app.active_mdb.get_diff(change_id)
    #logger.debug("diff: " + str(response))

    return render_template("data/change.html", change_id=change_id, change=response, data_type=data_type)

@data_app.route('/change/accept/<change_id>/<data_type>', methods=['GET'])
def accept_change(change_id, data_type):
    if data_type == "datastructure":
        message = "Datastructure accepted by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.approve_datastructure(change_id, message)
    elif data_type == "instance":
        message = "Instance accepted by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.approve_instance(change_id, message)
    return "success"

@data_app.route('/change/reject/<change_id>/<data_type>', methods=['GET'])
def reject_change(change_id, data_type):
    if data_type == "datastructure":
        message = "Datastructure rejected by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.reject_datastructure(change_id, message)
    elif data_type == "instance":
        message = "Instance rejected by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.reject_instance(change_id, message)
    return "success"
