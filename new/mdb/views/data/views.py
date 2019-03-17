from flask import Flask, Blueprint, request, json, render_template
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

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        return json_beautifier.dumps(json_beautifier.loads(json_thing), sort_keys=sort, indent=indents)
    else:
        return json_beautifier.dumps(json_thing, sort_keys=sort, indent=indents)

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

@data_app.route('/instance/<key>', methods=['GET', 'POST'])
def instance(key):
    response = data_app.active_mdb.retrieve_instance_from_database(key)
    data = json.loads(response)
    formatters= data_app.active_mdb.formatter_index()
    #[data["def_version"]]
    print("formatters",formatters)
    return render_template("data/instance.html", instance=response, key=key, formatters=formatters)

@data_app.route('/instances', methods=["GET"])
def instances():
    response = data_app.active_mdb.instance_index()
    return render_template("data/instances.html", instances=response)

@data_app.route('/definition/<key>',methods=['GET', 'POST'])
def definition(key):
    response = data_app.active_mdb.retrieve_definition(key)
    return render_template("data/definition.html", definition=response, key=key)

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

@data_app.route('/edit_instance', methods=["POST"])
def edit_instance():
    key = request.form['instanceKey']
    return "we got the key for instance: " + key

@data_app.route('/edit_definition', methods=["POST"])
def edit_definition():
    key = request.form['definitionKey']
    return "we got the key for definition: " + key