from flask import Flask, Blueprint, request, json, render_template, jsonify
from flask_login import current_user
from flask_login import login_required
from md.views.data import data_app
from md.core import logger
from werkzeug.utils import secure_filename
import os
import sys
import tarfile
import shutil # for removing directories recursive
import traceback # for error stack printing

import json as json_beautifier

##########################
##########################
##   API
##########################
##########################
@data_app.route('api/instance/<key>',methods=['GET', 'POST'])
@login_required
def api_instance(key):
    """ API endpoint to retrieve an instance from the database by its key.

    :param key: The key for the instance to retrieve.
    :returns: The instance retrieved from the database."""
    return data_app.active_mdb.retrieve_instance_from_database(key)

@data_app.route('api/instances', methods=["GET"])
@login_required
def api_instances():
    """ API endpoint to retrieve all instances from the database.

    :returns: A JSON array of all instances."""
    return "["+",".join(data_app.active_mdb.get_instances())+"]"

@data_app.route('api/datastructures', methods=["GET"])
@login_required
def api_datastructures():
    """ API endpoint to retrieve all datastructures from the database.

    :returns: A JSON array of all datastructures."""
    return "["+",".join(data_app.active_mdb.get_datastructures)+"]"

# function to get change list
@data_app.route('api/pendings', methods=["GET", "POST"])
@login_required
def api_pendings():
    """ API endpoint to retrieve a list of pending items (Datastructures, Instances, etc.).

    :returns: A JSON object with pending datastructures, instances, formatters, datasets, and formats."""
    response = {
        "Datastructures": data_app.active_mdb.pending_datastructures(),
        "Instances": data_app.active_mdb.pending_instances(),
        "Formatters": data_app.active_mdb.pending_formatters(),
        "Datasets": data_app.active_mdb.pending_datasets(),
        "Formats": data_app.active_mdb.pending_formats()
    }
    return jsonify(response)


@data_app.route('api/definition/<key>',methods=['GET', 'POST'])
@login_required
def api_definition(key):
    """ API endpoint to retrieve a definition from the database by its key.

    :param key: The key for the definition to retrieve.
    :returns: The definition retrieved from the database."""
    return data_app.active_mdb.retrieve_definition(key)

@data_app.route('api/definitions', methods=["GET"])
@login_required
def api_definitions():
    """ API endpoint to retrieve all definitions from the database.

    :returns: A list of all definitions."""
    return data_app.active_mdb.definition_index()

def pp_json(json_thing, sort=False, indents=4):
    """ Helper function to pretty-print JSON with custom indentation and sorting.

    :param json_thing: The JSON object to pretty-print.
    :param sort: Whether to sort keys in the output.
    :param indents: Number of spaces to use for indentation.
    :returns: The formatted JSON string."""
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

##############################################################################
########################## Instances  ########################################
##############################################################################


# retrieves an instance object
@data_app.route('/instance/<key>', methods=['GET', 'POST'])
def instance(key):
    response = data_app.active_mdb.retrieve_instance(key)
    # get actual json from json_dumps
    instance_data = json_beautifier.loads(response)

    out = {}

    #formatters = [ f.split(" ") for f in data_app.active_mdb.get_instances_by_datastructure(instance_data["datastructure"])]


    formatters = data_app.active_mdb.get_formatters_by_datastructure(instance_data["datastructure"])
    #formatters = [ f.split(" ") for f in data_app.active_mdb.get_formats_by_datastructure(instance_data["datastructure"])]
    # get html representation for instance object and add to output
    out["page"] = render_template("data/instance.html", instance=json_beautifier.dumps(instance_data, indent = 4, sort_keys=False), formatters =formatters, key=key)

    # add actual json to output
    out["data"] = instance_data

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

# function to list all instances
@data_app.route('/instances', methods=["GET"])
def instances():
    """API endpoint to retrieve an instance by its key and return both HTML and JSON representations.
    :param key: The key of the instance to retrieve.
    :returns: A JSON object containing the instance data and its HTML representation."""
    #  A dictionary of key-name pairs
    datastructures = {}
    for key in data_app.active_mdb.get_datastructures():
        datastructures[key]= json_beautifier.loads(data_app.active_mdb.retrieve_datastructure(key))["name"]
    return render_template("data/instances.html", datastructures=datastructures)

# function to list all instances of specific datastructure
@data_app.route('/instances_by_datastructure/<datastructure>', methods=["GET", 'POST'])
def instances_by_datastructure(datastructure):
    """Retrieves instances associated with a specific datastructure and renders an HTML list of those instances.
    Route: /instances_by_datastructure/<datastructure>
    Methods: GET, POST
    :param datastructure: The datastructure to filter instances by.
    :returns: An HTML page displaying a list of instances with their names."""
    #  A dictionary of key-name pairs

    instances = {}
    for key in data_app.active_mdb.get_instances_by_datastructure(datastructure):
        instances[key] =json_beautifier.loads(data_app.active_mdb.retrieve_instance(key))["name"]
    return render_template("data/instances_list.html", instances=instances)


@data_app.route('/create_instance/', methods=['GET', 'POST'])
def create_instance():
    """Displays a form to create a new instance, including a list of available datastructures.
    Route: /create_instance/
    Methods: GET, POST
    :returns: An HTML form for creating an instance, with available datastructures."""
    datastructures = {}
    for key in data_app.active_mdb.get_datastructures():
        datastructures[key]= json_beautifier.loads(data_app.active_mdb.retrieve_datastructure(key))["name"]
    return  render_template("data/create_instance.html", datastructures=datastructures)


@data_app.route('/instances_by_datastructure_for_dataset/<datastructure>', methods=["GET"])
def instances_by_datastructure_for_dataset(datastructure):
    """Displays a list of instances for a specific datastructure, for use with datasets.
    Route: /instances_by_datastructure_for_dataset/<datastructure>
    Methods: GET
    :param datastructure: The datastructure to filter instances by.
    :returns: An HTML page displaying a list of instances for the specified datastructure."""
    #  A dictionary of key-name pairs
    instances = {}
    for key in data_app.active_mdb.get_instances_by_datastructure(datastructure):
        instances[key] =json_beautifier.loads(data_app.active_mdb.retrieve_instance(key))["name"]
    return render_template("data/instances_list_for_dataset.html", instances=instances)

##############################################################################
########################## Datastructures ####################################
##############################################################################

# function to retrieve a datastructure
@data_app.route('/datastructure/<key>', methods=['GET', 'POST'])
def datastructure(key):
    """Retrieves and displays a datastructure based on the provided key.
    Route: /datastructure/<key>
    Methods: GET, POST
    :param key: The key of the datastructure to retrieve.
    :returns: A JSON object and an HTML page displaying the datastructure."""
    response = data_app.active_mdb.retrieve_datastructure(key)
    json_data = json_beautifier.loads(response)

    out = {}

    # get html representation for defnition object and add to output
    out["page"] = render_template("data/datastructure.html", datastructure=json_beautifier.dumps(json_data, indent = 4, sort_keys=False), key=key)

    # add actual json to output
    out["data"] = json_data

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

@data_app.route('/datastructures', methods=["GET"])
def datastructures():
    """Retrieves and displays all datastructures.
    Route: /datastructures
    Methods: GET
    :returns: A rendered HTML page displaying all datastructures."""
    #  A dictionary of key-name pairs
    datastructures = {}
    for key in data_app.active_mdb.get_datastructures():
        datastructures[key]= json_beautifier.loads(data_app.active_mdb.retrieve_datastructure(key))["name"]

    return render_template("data/datastructures.html", datastructures=datastructures)

@data_app.route('/create_datastructure/', methods=['GET', 'POST'])
def create_datastructure():
    """Displays the page for creating a new datastructure.
    Route: /create_datastructure/
    Methods: GET, POST
    :returns: A rendered HTML page for creating a new datastructure."""
    return  render_template("data/create_datastructure.html")


##############################################################################
########################## Datasets  #########################################
##############################################################################


# function to retrieve a datastructure
@data_app.route('/dataset/<key>', methods=['GET', 'POST'])
def dataset(key):
    """Retrieves and displays a dataset by its key.
    Route: /dataset/<key>
    Methods: GET, POST
    :param key: The key of the dataset to retrieve.
    :returns: A rendered HTML page displaying the dataset."""
    response = data_app.active_mdb.retrieve_dataset(key)
    #json_data = json_beautifier.loads(response)
    json_data = '{"%s":"%s"}' % (key, response)

    out = {}

    """# get html representation for defnition object and add to output
    out["page"] = render_template("data/dataset.html", dataset=json_beautifier.dumps(json_data, indent = 4, sort_keys=False), key=key)

    # add actual json to output
    out["data"] = json_data

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)"""
    #return render_template("data/dataset.html", dataset=json_beautifier.dumps(json_data, indent = 4, sort_keys=False), key=key)
    return render_template("data/dataset.html", dataset=response.split(','), key=key)

@data_app.route('/datasets/', methods=["GET"])
def datasets():
    """Displays all datasets available.
    Route: /datasets/
    Methods: GET
    :returns: A rendered HTML page displaying all datasets."""

    #  A dictionary of key-name pairs
    datasets = {}
    for key in data_app.active_mdb.get_datasets():
        retrieved_dataset = data_app.active_mdb.retrieve_dataset(key)
        datasets[key]= retrieved_dataset
        #datasets[key]= json_beautifier.loads(data_app.active_mdb.retrieve_dataset(key))["name"]

    return render_template("data/datasets.html", datasets=datasets)

@data_app.route('/create_dataset/', methods=['GET', 'POST'])
def create_dataset():
    """Displays a page to create a new dataset with available datastructures.
    Route: /create_dataset/
    Methods: GET, POST
    :returns: A rendered HTML page to create a new dataset."""
    datastructures = {}
    for key in data_app.active_mdb.get_datastructures():
        datastructures[key]= json_beautifier.loads(data_app.active_mdb.retrieve_datastructure(key))["name"]
    return  render_template("data/create_dataset.html", datastructures=datastructures)

@data_app.route('/add_dataset', methods=['POST'])
def add_dataset():
    """Adds a new dataset with selected instances.
    Route: /add_dataset
    Methods: POST
    :returns: A confirmation response."""
    instances_in_dataset = request.form.getlist("instanceList")
    data_app.active_mdb.add_dataset(instances_in_dataset, "Formatter created by " + current_user.email)
    return "ok"

##############################################################################
########################## Formatters ########################################
##############################################################################

@data_app.route('/create_formatter/', methods=['GET', 'POST'])
def create_formatter():
    """Displays a page to create a new formatter with available formats.
    Route: /create_formatter/
    Methods: GET, POST
    :returns: A rendered HTML page to create a new formatter."""
    formats = {}
    for key in data_app.active_mdb.get_formats():
        formats[key]= json_beautifier.loads(data_app.active_mdb.retrieve_format(key))["name"]
    return  render_template("data/create_formatter.html", formats=formats)

@data_app.route('/add_formatter', methods=["POST"])
def add_formatter():
    """Adds a new formatter with selected details.
    Route: /add_formatter
    Methods: POST
    :returns: A response with the result of adding the formatter."""
    formatter = request.form['formatter']
    formatter_name = request.form['name']
    from_datastructure = request.form['from_datastructure']
    to_datastructure = request.form['to_datastructure']

    message = "Formatter created by " + current_user.email

    response = data_app.active_mdb.add_formatter(formatter_name, formatter,from_datastructure, to_datastructure, message)

    logger.debug("response: " + str(response))
    return response


#   formatters page
@data_app.route('/formatters', methods=["GET"])
def formatters():
    """Displays a list of available formatters.
    Route: /formatters
    Methods: GET
    :returns: A rendered HTML page with a list of available formatters."""
    #  A dictionary of key-name pairs
    formats = {}
    for key in data_app.active_mdb.get_formats():
        formats[key]= json_beautifier.loads(data_app.active_mdb.retrieve_format(key))["name"]
    return render_template("data/formatters.html", formats=formats)


# retrieves an formatter object
@data_app.route('/formatter/<key>', methods=['GET', 'POST'])
def formatter(key):
    """Retrieves a formatter object by its key.
    Route: /formatter/<key>
    Methods: GET, POST
    :param key: The key of the formatter to retrieve
    :returns: A JSON response containing the formatter object and its HTML representation"""
    formatter = data_app.active_mdb.retrieve_formatter(key)

    out = {}

    # get html representation for instance object and add to output
    out["page"] = render_template("data/formatter.html", formatter=formatter, key=key)

    # add actual json to output
    out["data"] = formatter

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

# function to list all formatters of specific datastructure
@data_app.route('/formatters_by_datastructure/<datastructure>', methods=["GET"])
def formatters_by_datastructure(datastructure):
    """Lists all formatters of a specific datastructure.
    Route: /formatters_by_datastructure/<datastructure>
    Method: GET
    :param datastructure: The datastructure to list formatters for
    :returns: An HTML page displaying all formatters for the given datastructure"""
    #  A dictionary of key-name pairs
    formatters = {}
    for key in data_app.active_mdb.get_formatters_by_datastructure(datastructure):
        keys = key.split(" ")
        formatter= data_app.active_mdb.retrieve_formatter(keys[2])
        formatters[keys[2]] = keys[1]
    return render_template("data/formatters_list.html", formatters=formatters)

# function to list all formatters of specific datastructure
@data_app.route('/formatters_by_format/<format>', methods=["GET"])
def formatters_by_format(format):
    """Lists all formatters for a specific format.
    Route: /formatters_by_format/<format>
    Method: GET
    :param format: The format to list formatters for
    :returns: An HTML page displaying all formatters for the given format"""
    #  A dictionary of key-name pairs
    formatters = {}
    for key in data_app.active_mdb.get_formatters_by_format(format):
        key= key.split(" ")

        formatters[key[2]] = json_beautifier.loads(data_app.active_mdb.retrieve_format(key[1]))["name"]
    return render_template("data/formatters_list.html", formatters=formatters)


##############################################################################
########################## Formats ########################################
##############################################################################

@data_app.route('/create_format/', methods=['GET', 'POST'])
@login_required
def create_format():
    """Handles the creation of a new format.
    Route: /create_format/
    Method: GET, POST
    :returns: Renders the template for creating a format with a list of datastructures"""
    datastructures = {}
    for key in data_app.active_mdb.get_datastructures():
        datastructures[key]= json_beautifier.loads(data_app.active_mdb.retrieve_datastructure(key))["name"]
    return  render_template("data/create_format.html", datastructures=datastructures)

@data_app.route('/add_format', methods=["POST"])
@login_required
def add_format():
    """Adds a new format.
    Route: /add_format
    Method: POST
    :returns: The response after attempting to add the format"""
    
    name = request.form['name']
    datastructure = request.form['datastructure']
    description = request.form['description']

    message = "Format created by " + current_user.email
    data = {"name":name,"datastructure":datastructure,"description":description}
    data = json_beautifier.dumps(data)
    print("data:",data)
    response = data_app.active_mdb.add_format(data, message)
    print("response:",response)

    logger.debug("response: " + str(response))
    return response

# function to list all formatters
@data_app.route('/formats', methods=["GET"])
def formats():
    """Lists all the datastructures for formatters.
    Route: /formats
    Method: GET
    :returns: Renders the formats page with a dictionary of datastructures"""
    #  A dictionary of key-name pairs
    datastructures = {}
    for key in data_app.active_mdb.get_datastructures():
        datastructures[key]= json_beautifier.loads(data_app.active_mdb.retrieve_datastructure(key))["name"]
    return render_template("data/formats.html", datastructures=datastructures)


# retrieves an format object
@data_app.route('/format/<key>', methods=['GET', 'POST'])
def format(key):
    """Retrieves a specific format object.
    Route: /format/<key>
    Method: GET, POST
    :param key: The key of the format to retrieve
    :returns: A JSON representation of the format with HTML page"""
    format = data_app.active_mdb.retrieve_format(key)

    out = {}

    # get html representation for instance object and add to output
    out["page"] = render_template("data/format.html", format=format, key=key)

    # add actual json to output
    out["data"] = format

    # return data with jsonify. otherwise the json object won't go correctly
    return jsonify(out)

# function to list all formatters of specific datastructure
@data_app.route('/formats_by_datastructure/<datastructure>', methods=["GET"])
def formats_by_datastructure(datastructure):
    """Lists all formats of a specific datastructure.
    Route: /formats_by_datastructure/<datastructure>
    Method: GET
    :param datastructure: The datastructure to list formats for
    :returns: Renders the formats list page with a dictionary of formats"""

    #  A dictionary of key-name pairs
    formats = {}
    for key in data_app.active_mdb.get_formats_by_datastructure(datastructure):
        formats[key] =json_beautifier.loads(data_app.active_mdb.retrieve_format(key))["name"]
    return render_template("data/formats_list.html", formats=formats)

##############################################################################
##############################################################################
##############################################################################

@data_app.route('/add_instance', methods=["POST"])
def add_instance():
    """Adds a new instance to the database.
    Route: /add_instance
    Method: POST
    :returns: Response indicating success or failure"""
    
    body = request.form['body']
    body = body[1:-1]

    message = "Instance created by " + current_user.email

    response = data_app.active_mdb.add_instance(body, message)
    logger.debug("response: " + str(response))

    return response


@data_app.route('/add_datastructure', methods=["POST"])
def add_datastructure():
    """Adds a new datastructure to the database.
    Route: /add_datastructure
    Method: POST
    :returns: Response indicating success or failure"""
    body = request.form['body']
    body = body[1:-1]

    message = "Datastructure created by " + current_user.email

    response = data_app.active_mdb.add_datastructure(body, message)
    print(response)

    logger.debug("response: " + str(response))

    return response

@data_app.route('/add_instance_data_field', methods=["GET"])
def add_instance_data_field():
    """Renders the page to add a data field to an instance.
    Route: /add_instance_data_field
    Method: GET
    :returns: Renders the data field add instance page"""
    return render_template("data/data_field_add_instance.html")


# this method is called when the edit button is clicked for instances
# input is the edited instance object
@data_app.route('/edit_instance', methods=["POST"])
def edit_instance():
    """Edits an existing instance in the database.
    Route: /edit_instance
    Method: POST
    :returns: Response indicating success or failure"""
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
    """Edits an existing datastructure in the database.
    Route: /edit_datastructure
    Method: POST
    :returns: Response indicating success or failure"""
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
@login_required
def editor_page():
    """Displays the editor page with all the pending changes in different categories.
    Route: /editor
    Method: GET, POST
    :returns: Rendered editor page with pending changes"""
    if not current_user.has_role('admin'): 
        return jsonify({"error": "Access denied, you are not an admin."}), 403
    pending_datastructures = data_app.active_mdb.pending_datastructures()
    pending_instances = data_app.active_mdb.pending_instances()
    pending_formatters = data_app.active_mdb.pending_formatters()
    pending_datasets = data_app.active_mdb.pending_datasets()
    pending_formats = data_app.active_mdb.pending_formats()

    return render_template("data/editor.html", datastructures=pending_datastructures, instances=pending_instances, formatters=pending_formatters, datasets=pending_datasets, formats=pending_formats)

# method that gets a change's details by id
@data_app.route('/change/<change_id>/<data_type>', methods=['GET'])
@login_required
def get_change(change_id, data_type):
    """Displays the details of a specific change based on its change_id and data_type.
    Route: /change/<change_id>/<data_type>
    Method: GET
    :param change_id: ID of the change to fetch
    :param data_type: Type of the data being changed
    :returns: Rendered change page with details of the change"""
    response = data_app.active_mdb.get_diff(change_id)
    #logger.debug("diff: " + str(response))

    return render_template("data/change.html", change_id=change_id, change=response, data_type=data_type)

@data_app.route('/change/accept/<change_id>/<data_type>', methods=['GET'])
@login_required
def accept_change(change_id, data_type):
    """Handles the acceptance of a change.
    Route: /change/accept/<change_id>/<data_type>
    Method: GET
    :param change_id: ID of the change to accept
    :param data_type: Type of the data being changed (datastructure, instance, formatter, dataset, format)
    :returns: Success message indicating change acceptance"""
    if data_type == "datastructure":
        message = "Datastructure accepted by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.approve_datastructure(change_id, message)
    if data_type == "instance":
        message = "Instance accepted by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.approve_instance(change_id, message)
    if data_type == "formatter":
        message = "Formatter accepted by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.approve_formatter(change_id, message)
    if data_type == "dataset":
        message = "Dataset accepted by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.approve_dataset(change_id, message)
    if data_type == "format":
        message = "Format accepted by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.approve_format(change_id, message)
    return "success"

@data_app.route('/change/reject/<change_id>/<data_type>', methods=['GET'])
@login_required
def reject_change(change_id, data_type):
    """Handles the rejection of a change.
    Route: /change/reject/<change_id>/<data_type>
    Method: GET
    :param change_id: ID of the change to reject
    :param data_type: Type of the data being changed (datastructure, instance, formatter, dataset)
    :returns: Success message indicating change rejection"""
    if data_type == "datastructure":
        message = "Datastructure rejected by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.reject_datastructure(change_id, message)
    if data_type == "instance":
        message = "Instance rejected by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.reject_instance(change_id, message)
    if data_type == "formatter":
        message = "Formatter rejected by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.reject_formatter(change_id, message)
    if data_type == "dataset":
        message = "Dataset rejected by " + current_user.email # TODO: get a message from ui
        data_app.active_mdb.reject_dataset(change_id, message)
    return "success"


@data_app.route('/format_instance/<instance>/<formatter>', methods=["GET"])
def formaformat_instancet(instance,formatter):
    """Applies a formatter to the specified instance.
    Route: /format_instance/<instance>/<formatter>
    Method: GET
    :param instance: ID of the instance to format
    :param formatter: ID of the formatter to apply
    :returns: Formatted instance based on the provided formatter"""
    return data_app.active_mdb.format_instance(instance,formatter)


##############################################################################
###################### Import ###########################################
##############################################################################

@data_app.route('/import', methods=["GET"])
def import_page():
    """Renders the import page with a list of available formats.
    Route: /import
    Method: GET
    Retrieves a list of formats from the database and displays them on the import page.
    Returns: Rendered HTML page with the list of formats."""

    formats = {}
    for key in data_app.active_mdb.get_formats():
        formats[key]= json_beautifier.loads(data_app.active_mdb.retrieve_format(key))["name"]
    return render_template("data/import.html", formats=formats)

@data_app.route('/import_file', methods=["POST"])
def import_file():
    """Handles the uploading and formatting of files based on user selections.
    Route: /import_file
    Method: POST
    :param files: Files uploaded by the user to be imported and formatted.
    :param from: The original format of the file.
    :param to: The target format to which the file should be converted.
    Returns: Success message if the import and formatting are successful, error message if any issue occurs."""
    initial_directory = os.getcwd()
    if request.method == 'POST':
          files = request.files.getlist('file')
          os.chdir("import_scratch")
          try:
              for f in files:
                fname = secure_filename(f.filename)
                os.mkdir(fname)
                os.chdir(fname)
                f.save(fname)

                print("About to db call")
                if request.form['from'] != request.form["to"]:
                  data_app.active_mdb.format_file(fname, request.form['from'], request.form["to"])
                # format_file changes directory
                os.chdir( os.path.join(initial_directory, "import_scratch") )
          except Exception as e:
              os.chdir(initial_directory)
              return 'Import failed: ' + traceback.format_exc()
          return 'Imported successfully'
    os.chdir(initial_directory)
    return "Import failed"


@data_app.route('/import_dataset', methods=["POST"])
def import_dataset():
    """Handles the uploading and importing of a dataset.
    Route: /import_dataset
    Method: POST
    :param file: The dataset file uploaded by the user.
    :param script: The script associated with the dataset import.
    :param from: The original format of the dataset.
    :param to: The target format for the dataset.
    Returns: Success message if the import is successful, failure message if an issue occurs."""
    if request.method == 'POST':
          f = request.files['file']
          fname = secure_filename(f.filename)
          os.chdir("import_scratch")
          os.mkdir(fname)
          os.chdir(fname)
          f.save(fname)

          data_app.active_mdb.import_dataset(fname,  request.form['script'], request.form['from'], request.form["to"])
          return 'Imported successfully'
    return "Import failed"
