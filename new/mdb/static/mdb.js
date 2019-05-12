var current_definition="";

function show_instance(key){
    $.get('/data/instance/'+ key, {}).done(function(response) {
        document.getElementById("data-display-area").innerHTML = response["page"];
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

function show_definition(key){
    $.get('/data/definition/'+ key, {}).done(function(response) {
        document.getElementById("data-display-area").innerHTML = response["page"];
        document.getElementById("jsonArea").appendChild(renderjson.set_show_to_level(2)(response["data"]));
    }).fail(function() {
        document.getElementById("data-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}


function register_definition(key){
    current_definition=key;
    document.getElementById("label_for_data_area").innerText = "Input for "+ current_definition;

}

function get_definitions(action) {
    $.get('/data/definitions/'+action, {}).done(function(response) {
        document.getElementById("list-display-area").innerHTML = response;
    }).fail(function() {
        document.getElementById("list-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}


function enable_edit(btnId, textAreaId, key) {
    var textArea = document.getElementById(textAreaId);
    textArea.style.visibility = "visible";

    $("#" + btnId).html("Commit Changes");

    var functionName = "edit_instance";
    if (btnId === "editDefinitionBtn")
        functionName = "edit_definition";
        
    $("#" + btnId).attr("onClick", functionName + "('" + key + "')");
}

function edit_instance(instanceKey) {
    $.post('/data/edit_instance', {instanceKey}).done(function(response) {
        console.log(response);
    }).fail(function() {
        console.log("we got error");
    });
}

function edit_definition(definitionKey) {
    $.post('/data/edit_definition', {definitionKey}).done(function(response) {
        console.log(response);
    }).fail(function() {
        console.log("we got error");
    });
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
 
function get_change(change_id) {
    $.get('/data/change/'+ change_id, {}).done(function(response) {
        document.getElementById("change-display-area").innerHTML =  response;
    }).fail(function() {
        document.getElementById("change-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}
