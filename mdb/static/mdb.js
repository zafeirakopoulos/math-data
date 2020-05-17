var current_definition="";

// this function called when an instance is clicked
function show_instance(key) {
    // perform a get request to the flask
    $.get('/data/instance/'+ key, {}).done(function(response) {
        // put the instance's html to the 'data-display-area' div
       document.getElementById("data-display-area").innerHTML = response["page"];

        // generate the collapsible json with renderjson and put it to 'jsonArea' div
       document.getElementById("jsonArea").appendChild(renderjson.set_show_to_level(2)(response["data"]));


    }).fail(function() {
        document.getElementById("data-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}

function get_instances() {
    $.get('/data/instances', {}).done(function(response) {
        document.getElementById("list-display-area").innerHTML = response;
    }).fail(function() {
        document.getElementById("list-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}


function view_json(jsObj) {
    return JSON.stringify(jsObj, null, 4);
}


// function that is called when a definition clicked
function show_datastructure(key){
    // request to flask to get the definition data
    $.get('/data/datastructure/'+ key, {}).done(function(response) {
        // put the html that generated to represent definition in to the "data-display-area" div
        document.getElementById("data-display-area").innerHTML = response["page"];

        // generate the collapsible json with renderjson and put it to 'jsonArea' div
        document.getElementById("jsonArea").appendChild(renderjson.set_show_to_level(2)(response["data"]));
    }).fail(function() {
        document.getElementById("data-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}

function register_definition(key){
    current_definition=key;
    document.getElementById("label_for_data_area").innerText = "Input for "+ current_definition;

}


// activates the edit button (this is called when user logged in)

// btnId: id of edit button that will be activated
// textAreaId: text area that the edit operation will be done
// key: attach the data's key to the button
function enable_edit(btnId, textAreaId, key) {
    var textArea = document.getElementById(textAreaId);
    textArea.style.display = "initial";

    $("#" + btnId).html("Commit Changes");

    var functionName = "edit_instance";
    if (btnId === "editdatastructureBtn")
        functionName = "edit_datastructure";

    $("#" + btnId).attr("onClick", functionName + "('" + key + "', '" + textAreaId + "')");
}


// function that is called when an instance object edited
function edit_instance(instanceKey, textAreaId) {
    let infoText = get_init_element("infoText");

    let body = $("#" + textAreaId).val();
    if(!isValidJson(body)) {
        print_input_error(infoText);
        return;
    }

    let data = {
        "instanceKey": instanceKey,
        "body": '"' + body + '"'
    };

    $.post('/data/edit_instance', data).done(function(response) {
        print_input_success(infoText);
    }).fail(function() {
        console.log("we got error");
    });
}


// function that is called when an definition object edited
function edit_datastructure(datastructureKey, textAreaId) {
    let infoText = get_init_element("infoText");

    let body = $("#" + textAreaId).val();
    if(!isValidJson(body)) {
        print_input_error(infoText);
        return;
    }

    let data = {
        "datastructureKey": datastructureKey,
        "body": '"' + body + '"'
    };

    $.post('/data/edit_datastructure', data).done(function(response) {
        print_input_success(infoText);
    }).fail(function(err) {
        console.log("we got error");
        console.log(err);
    });
}

function create(textAreaId) {
    let infoText = get_init_element("infoText");

    let body = $("#" + textAreaId).val();
    let selectedType = $("input:checked").val();

    if(!isValidJson(body)) {
        print_input_error(infoText);
        return;
    }

    if (selectedType === 'datastructure' || selectedType === 'instance') {
        let url = '/data/add_' + selectedType;
        let data = {
            "body": '"' + body + '"'
        }

        $.post(url, data).done(function(response) {
            print_input_success(infoText);
        }).fail(function(err) {
            console.log("we got error while creating...");
            console.log(err);
        });
    }
}

function add_definition(key){
    $.get('/data/definition/'+ key, {}).done(function(response) {
        document.getElementById("data-display-area").innerHTML =  response;
    }).fail(function() {
        document.getElementById("data-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}

function add_instance(){
    $.get('/data/definitions/create_instance', {}).done(function(response_definitions) {
        document.getElementById("list-display-area").innerHTML = response_definitions;
    }).fail(function() {
        document.getElementById("list-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });

    $.get('/data/add_instance_data_field', {}).done(function(response_input_field) {
        document.getElementById("data-display-area").innerHTML = response_input_field;
    }).fail(function() {
        document.getElementById("data-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}


// function that is called when a change selected from change-list.
// gets the change detail to show.
function get_change(change_id, data_type) {
    $.get('/data/change/'+ change_id + '/' + data_type, {}).done(function(response) {
        document.getElementById("change-display-area").innerHTML =  response;
    }).fail(function(err) {
        document.getElementById("change-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
        console.log(err);
    });
}

function accept_change(change_id, data_type) {
    $.get('/data/change/accept/'+ change_id + '/' + data_type, {}).done(function(response) {
        document.getElementById("change-display-area").innerHTML =  "Accepted!";
    }).fail(function(err) {
        document.getElementById("change-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
        console.log(err);
    });
}

function reject_change(change_id, data_type) {
    $.get('/data/change/reject/'+ change_id + '/' + data_type, {}).done(function(response) {
        document.getElementById("change-display-area").innerHTML =  "Rejected!";
    }).fail(function(err) {
        document.getElementById("change-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
        console.log(err);
    });
}

function isValidJson(text){
    if (typeof text !== "string"){
        return false;
    }

    try{
        JSON.parse(text);
        return true;
    }
    catch (error){
        return false;
    }
}

function get_init_element(elementId) {
    let infoElement = document.getElementById(elementId);
    infoElement.style.display = "none";
    return infoElement;
}

function print_input_error(element) {
    element.style.display = "initial";
    element.style.color = "red";
    element.innerHTML = "Your input is not a valid JSON.";
}

function print_input_success(element) {
    element.style.display = "initial";
    element.style.color = "green";
    element.innerHTML = "Successfull";
}
