from flask import Flask, Blueprint, request, json, render_template, jsonify
from mdb.views.data import data_app

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
    return data_app.active_mdb.instance_index()

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
@data_app.route('/',methods=['GET', 'POST'])
def index():
    return render_template("data/index.html")


@data_app.route('/browse',methods=['GET', 'POST'])
def browse():
    return render_template("data/browse.html")


@data_app.route('/create',methods=['GET', 'POST'])
def create():
    return render_template("data/create.html")

@data_app.route('/edit',methods=['GET', 'POST'])
def edit():
    return render_template("data/edit.html")

# retrieves an instance object
@data_app.route('/instance/<key>', methods=['GET', 'POST'])
def instance(key):
    response = data_app.active_mdb.retrieve_instance_from_database(key)
    formatters = data_app.active_mdb.formatter_index()

    # get actual json from json_dumps
    json_data = json_beautifier.loads(response)

    out = {}
    
    # get html representation for instance object and add to output
    out["page"] = render_template("data/instance.html", instance=json_beautifier.dumps(json_data, indent = 4, sort_keys=False), key=key, formatters=formatters)
    
    # add actual json to output
    out["data"] = json_data
    
    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

# function to list all instances
@data_app.route('/instances', methods=["GET"])
def instances():
    response = data_app.active_mdb.instance_index()
    return render_template("data/instances.html", instances=response)

# function to retrieve a definition
@data_app.route('/definition/<key>', methods=['GET', 'POST'])
def definition(key):
    response = data_app.active_mdb.retrieve_definition(key)

    # get actual json from json_dumps
    json_data = json_beautifier.loads(response)

    out = {}

    # get html representation for defnition object and add to output
    out["page"] = render_template("data/definition.html", definition=json_beautifier.dumps(json_data, indent = 4, sort_keys=False), key=key)
    
    # add actual json to output
    out["data"] = json_data

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

@data_app.route('/definitions/<action>', methods=["GET"])
def definitions(action):
    if action=="create_instance":
        action="register"
    if action=="browse_definitions":
        action="show"

    response = data_app.active_mdb.definition_index()
    return render_template("data/definitions.html", definitions=response, action=action)

@data_app.route('/add_instance', methods=["POST"])
def add_instance():

    content = request.form
    #print("=========================")
    #print( request.args)
    #print( request.form)
    #print( request.values)

    response = data_app.active_mdb.add_instance_to_database(content)
    js = json.dumps()
    return js

@data_app.route('/add_instance_data_field', methods=["GET"])
def add_instance_data_field():
    return render_template("data/data_field_add_instance.html")


# this method is called when the edit button is clicked for instances
# input is the edited instance object
@data_app.route('/edit_instance', methods=["POST"])
def edit_instance():
    # TODO: fill this function to actually send edit request to backend
    key = request.form['instanceKey']
    return "we got the key for instance: " + key


# this method is called when the edit button is clicked for definitions
# input is the edited definition object
@data_app.route('/edit_definition', methods=["POST"])
def edit_definition():
    # TODO: fill this function to actually send edit request to backend
    key = request.form['definitionKey']
    return "we got the key for definition: " + key


# function to get change list
@data_app.route('/editor', methods=["GET", "POST"])
def editor_page():
    change1 = {
        'change_name': 'Change 1',
        'change_date': '13.10.2019',
        'change_owner': 'elif@elif.com',
        'change_id': '123456'
    }

    change2 = {
        'change_name': 'Change 2',
        'change_date': '13.09.2019',
        'change_owner': 'xyz@xyz.com',
        'change_id': '987665'
    }

    # TODO: get actual change list from backend and show in frontend
    change_list = [change1, change2]
    return render_template("data/editor.html", changes=change_list)


# method that gets a change's details by id
@data_app.route('/change/<change_id>', methods=['GET'])
def get_change(change_id):
    change = {
        'change_name': 'A Change',
        'change_date': '13.10.2019',
        'change_owner': 'ea@ea.com',
        'change_id': change_id,
        'change_body': 'There will be a diff showing the differences. Now it is just a text to demonstrate.ksdgsdfssnfoeıfm23dm239dj239dj293dj329fnıdsjfksfjskdfhk32hfufn28fhu28ufh2efhı2fhksjfjksdfhe2ufnvn28evn8vn8vnsuıdvnskdvnsdk'
    }
    
    # TODO: get actual change data from backend
    return render_template("data/change.html", change=change)