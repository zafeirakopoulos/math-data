var current_definition="";

function show_instance(key){
    $.get('/data/instance/'+ key, {}).done(function(response) {
        document.getElementById("data-display-area").innerHTML = response;
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

function show_definition(key){
    $.get('/data/definition/'+ key, {}).done(function(response) {
        document.getElementById("data-display-area").innerHTML =  "<pre><code class=\"json\">"+ response + "</code></pre>";
        console.log(document.getElementById("data-display-area").innerHTML);
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
 
