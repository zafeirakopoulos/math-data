var current_definition="";

// this function called when an instance is clicked
function show_instance(key) {
    // perform a get request to the flask
    $.get('/data/instance/'+ key, {}).done(function(response) {
        // put the instance's html to the 'data-display-area' div
        document.getElementById("data-display-area").innerHTML = response["page"];

        // generate the collapsible json with renderjson and put it to 'jsonArea' div
        document.getElementById("jsonArea").appendChild(renderjson.set_show_to_level(2)(response["data"]));

        // initialize the visual part as empty
        document.getElementById("graph-container").innerHTML = "";

        // TODO: generate graph object with real definition and data
        // get edges array from graph json
        const edges = response["data"]["raw"]["dense"]["edges"];
        if (edges) {
            let i = 0, j = 0, c = 0;

            // graph data object to use when generating visual
            let g = {
                nodes: [],
                edges: []
            };

            // generate nodes of graph
            for (; i < edges.length; ++i) {
                // we are setting random x,y positions and random size to each node
                // we are using index as id of node
                g.nodes.push({
                    id: i,
                    label: 'Node ' + i,
                    x: Math.floor(Math.random() * 300),
                    y: Math.floor(Math.random() * 300),
                    size: Math.floor(Math.random() * 10),
                    color: '#666'
                });
            }

            // generate edges with edges array
            for (i = 0; i < edges.length; ++i) {
                let connections = edges[i];
                j = 0;
                for (; j < connections.length; ++j) {
                    if (connections[j] != 0) {
                        // setting random sizes
                        g.edges.push({
                            id: 'e' + c,
                            source: i,
                            target: j,
                            size: Math.random(),
                            color: '#ccc'
                        });
                        
                        c++;
                    }
                }
            }
            
            // call sigmajs to generate graph visual
            // we are telling sigma to put the generated visual in to 'graph-container' div
            s = new sigma({
                graph: g,
                renderer: {
                    container: document.getElementById('graph-container'),
                    type: 'canvas'
                }
            });
        }

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
function show_definition(key){
    // request to flask to get the definition data
    $.get('/data/definition/'+ key, {}).done(function(response) {
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

function get_definitions(action) {
    $.get('/data/definitions/'+action, {}).done(function(response) {
        document.getElementById("list-display-area").innerHTML = response;
    }).fail(function() {
        document.getElementById("list-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
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
    if (btnId === "editDefinitionBtn")
        functionName = "edit_definition";
        
    $("#" + btnId).attr("onClick", functionName + "('" + key + "')");
}


// function that is called when an instance object edited
function edit_instance(instanceKey) {
    $.post('/data/edit_instance', {instanceKey}).done(function(response) {
        console.log(response);
    }).fail(function() {
        console.log("we got error");
    });
}


// function that is called when an definition object edited
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


// function that is called when a change selected from change-list.
// gets the change detail to show.
function get_change(change_id) {
    $.get('/data/change/'+ change_id, {}).done(function(response) {
        document.getElementById("change-display-area").innerHTML =  response;
    }).fail(function() {
        document.getElementById("change-display-area").innerHTML = "{{ 'Error: Could not contact server.' }}";
    });
}
