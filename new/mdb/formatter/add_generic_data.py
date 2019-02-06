import json
import string
import os
import sys
import collections
from tulip import tlp
from pprint import pprint
new_path = sys.path[0]
new_path = new_path[:-10] + "/language/"
sys.path[0] = new_path
path_def = new_path[:-18] + "/local/defs/"
new_path = new_path[:-18] + "/local/third_party/"
PATH = new_path   #should be changed
print(PATH)


def add_data_devwg(file_name, raw_types):
    file = open(PATH+file_name, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

            # to create an empty list
            graph_list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                graph_list[i] = [0] * 3

            # for vertices
            vertices_list = [0] * int(number_nodes)

        values= []
        if each_line[0] == "e":
            #e, nv, ne, ew = each_line.split()
            values = each_line.split()

            adj_matrix[int(values[1]) - 1][int(values[2]) - 1] = int(values[3])  # upper triangular matrix
            adj_matrix[int(values[2])-1][int(values[1])-1] = int(values[3])     # lower triangular matrix

            graph_list[counter][0] = int(values[1])
            graph_list[counter][1] = int(values[2])
            graph_list[counter][2] = int(values[3])
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)
		
    with open(path_def+"graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Directed Edge and Vertex Weighted Graph")
        data = setPlural(data, "Directed Edge and Vertex Weighted Graphs")
        options = dict({
			"vertices": {
			           "weighted": True
			},
			"edges": {
			           "directed": True,
					   "weighted": True
			}
        })
        data = setRawTypes(data, raw_types)
        data = setAttributes(data, ["edges", "vertices"])
        data = setOptions(data, options)
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        raw = dict()
        if isinstance(raw_types, list):
            for raw_type in raw_types:
                if raw_type == "dense":
                    raw["dense"] = {"edges": adj_matrix, "vertices": vertices_list}
                if raw_type == "sparse":
                    raw["sparse"] = {"edges": graph_list, "vertices": vertices_list}  
        else:
            if raw_types == "dense":
                raw["dense"] = {"edges": adj_matrix, "vertices": vertices_list}
            else:
                raw["sparse"] = {"edges": graph_list, "vertices": vertices_list}                      
        data = setRaw(data, raw)
    createOutput(raw_types, data, "Directed Edge and Vertex Weighted Graph", file_name)

def add_data_evwg(file_name, raw_types):
    file = open(PATH+file_name, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

            # to create an empty list
            graph_list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                graph_list[i] = [0] * 3

            # for vertices
            vertices_list = [0] * int(number_nodes)

        values= []
        if each_line[0] == "e":
            #e, nv, ne, ew = each_line.split()
            values = each_line.split()

            adj_matrix[int(values[1]) - 1][int(values[2]) - 1] = int(values[3])  # upper triangular matrix
            adj_matrix[int(values[2])-1][int(values[1])-1] = int(values[3])     # lower triangular matrix

            graph_list[counter][0] = int(values[1])
            graph_list[counter][1] = int(values[2])
            graph_list[counter][2] = int(values[3])
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)
		
    with open(path_def+"graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Edge and Vertex Weighted Graph")
        data = setPlural(data, "Edge and Vertex Weighted Graphs")
        options = dict({
			"vertices": {
			           "weighted": True
			},
			"edges": {
			           "weighted": True
			}
        })

        data = setRawTypes(data, raw_types)
        data = setAttributes(data, ["edges", "vertices"])
        data = setOptions(data, options)
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        raw = dict()
        if isinstance(raw_types, list):
            for raw_type in raw_types:
                if raw_type == "dense":
                    raw["dense"] = {"edges": adj_matrix, "vertices": vertices_list}
                if raw_type == "sparse":
                    raw["sparse"] = {"edges": graph_list, "vertices": vertices_list}  
        else:
            if raw_types == "dense":
                raw["dense"] = {"edges": adj_matrix, "vertices": vertices_list}
            else:
                raw["sparse"] = {"edges": graph_list, "vertices": vertices_list}                      
        data = setRaw(data, raw)
    createOutput(raw_types, data, "Edge and Vertex Weighted Graph", file_name)
	
def add_data_dvwg(file_name, raw_types):
    file = open(PATH+file_name, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

            # to create an empty list
            graph_list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                graph_list[i] = [0] * 2

            # for vertices
            vertices_list = [0] * int(number_nodes)

        values= []
        if each_line[0] == "e":
            #e, nv, ne, ew = each_line.split()
            values = each_line.split()

            adj_matrix[int(values[1]) - 1][int(values[2]) - 1] = 1  # upper triangular matrix
            adj_matrix[int(values[2])-1][int(values[1])-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(values[1])
            graph_list[counter][1] = int(values[2])
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)
		
    with open(path_def+"graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Directed Vertex Weighted Graph")
        data = setPlural(data, "Directed Vertex Weighted Graphs")
        options = dict({
			"vertices": {
			           "weighted": True
			},
			"edges": {
			           "directed": True
			}
        })
        data = setRawTypes(data, raw_types)
        data = setAttributes(data, ["edges", "vertices"])
        data = setOptions(data, options)
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        raw = dict()
        if isinstance(raw_types, list):
            for raw_type in raw_types:
                if raw_type == "dense":
                    raw["dense"] = {"edges": adj_matrix, "vertices": vertices_list}
                if raw_type == "sparse":
                    raw["sparse"] = {"edges": graph_list, "vertices": vertices_list}  
        else:
            if raw_types == "dense":
                raw["dense"] = {"edges": adj_matrix, "vertices": vertices_list}
            else:
                raw["sparse"] = {"edges": graph_list, "vertices": vertices_list}                      
        data = setRaw(data, raw)
    createOutput(raw_types, data, "Directed Vertex Weighted Graph", file_name)


def add_data_dewg(file_name, raw_types):
    file = open(PATH+file_name, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

            # to create a empty list
            graph_list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                graph_list[i] = [0] * 3

        values= []
        if each_line[0] == "e":
            #e, nv, ne, ew = each_line.split()
            values = each_line.split()

            adj_matrix[int(values[1]) - 1][int(values[2]) - 1] = int(values[3])  # upper triangular matrix
            adj_matrix[int(values[2])-1][int(values[1])-1] = int(values[3])     # lower triangular matrix

            graph_list[counter][0] = int(values[1])
            graph_list[counter][1] = int(values[2])
            graph_list[counter][2] = int(values[3])
            counter += 1

    with open(path_def+"graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Directed Edge Weighted Graph")
        data = setPlural(data, "Directed Edge Weighted Graphs")
        options = dict({
			"edges": {
			           "weighted": True,
			           "directed": True
			}
        })
        data = setRawTypes(data, raw_types)

        data = setAttributes(data, ["edges"])
        data = setOptions(data, options)
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        raw = dict()
        if isinstance(raw_types, list):
            for raw_type in raw_types:
                if raw_type == "dense":
                    raw["dense"] = {"edges": adj_matrix}
                if raw_type == "sparse":
                    raw["sparse"] = {"edges": graph_list}  
        else:
            if raw_types == "dense":
                raw["dense"] = {"edges": adj_matrix}
            else:
                raw["sparse"] = {"edges": graph_list}                      
        data = setRaw(data, raw)
    createOutput(raw_types, data, "Directed Edge Weigthed Graph", file_name)


def add_data_vwg(file_name, raw_types):
    file = open(PATH+ file_name, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

            # to create an empty list
            graph_list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                graph_list[i] = [0] * 2

            # for vertices
            vertices_list = [0] * int(number_nodes)

        values= []
        if each_line[0] == "e":
            #e, nv, ne, ew = each_line.split()
            values = each_line.split()

            adj_matrix[int(values[1]) - 1][int(values[2]) - 1] = 1  # upper triangular matrix
            adj_matrix[int(values[2])-1][int(values[1])-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(values[1])
            graph_list[counter][1] = int(values[2])
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)
		
    with open(path_def+"graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Vertex Weighted Graph")
        data = setPlural(data, "Vertex Weighted Graphs")
        options = dict({
			"vertices": {
			           "weighted": True
			}
        })
        data = setRawTypes(data, raw_types)

        data = setAttributes(data, ["edges", "vertices"])
        data = setOptions(data, options)
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        raw = dict()
        if isinstance(raw_types, list):
            for raw_type in raw_types:
                if raw_type == "dense":
                    raw["dense"] = {"edges": adj_matrix, "vertices": vertices_list}
                if raw_type == "sparse":
                    raw["sparse"] = {"edges": graph_list, "vertices": vertices_list}  
        else:
            if raw_types == "dense":
                raw["dense"] = {"edges": adj_matrix, "vertices": vertices_list}
            else:
                raw["sparse"] = {"edges": graph_list, "vertices": vertices_list}                      
        data = setRaw(data, raw)
    createOutput(raw_types, data, "Vertex Weighted Graph", file_name)
			
		
def add_data_ewg(file_name, raw_types):
    file = open(PATH+file_name, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

            # to create a empty list
            graph_list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                graph_list[i] = [0] * 3
        values= []
        if each_line[0] == "e":
            #e, nv, ne, ew = each_line.split()
            values = each_line.split()

            adj_matrix[int(values[1]) - 1][int(values[2]) - 1] = int(values[3])  # upper triangular matrix
            adj_matrix[int(values[2])-1][int(values[1])-1] = int(values[3])     # lower triangular matrix

            graph_list[counter][0] = int(values[1])
            graph_list[counter][1] = int(values[2])
            graph_list[counter][2] = int(values[3])
            counter += 1

    with open(path_def+"graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Edge Weighted Graph")
        data = setPlural(data, "Edge Weighted Graphs")
        options = dict({

		"edges": {
		           "weighted": True
			}
        })
        data = setRawTypes(data, raw_types)
        data = setAttributes(data, ["edges"])
        data = setOptions(data, options)
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        raw = dict()
        if isinstance(raw_types, list):
            for raw_type in raw_types:
                if raw_type == "dense":
                    raw["dense"] = {"edges": adj_matrix}
                if raw_type == "sparse":
                    raw["sparse"] = {"edges": graph_list}  
        else:
            if raw_types == "dense":
                raw["dense"] = {"edges": adj_matrix}
            else:
                raw["sparse"] = {"edges": graph_list}                      
        data = setRaw(data, raw)
    createOutput(raw_types, data, "Edge Weighted Graph", file_name)



			

def add_data_dg(file_name, raw_types):
    file = open(PATH+file_name, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

            # to create a empty list
            graph_list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                graph_list[i] = [0] * 2

        values= []
        if each_line[0] == "e":
            #e, nv, ne, ew = each_line.split()
            values = each_line.split()

            adj_matrix[int(values[1]) - 1][int(values[2]) - 1] = 1  # upper triangular matrix
            adj_matrix[int(values[2])-1][int(values[1])-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(values[1])
            graph_list[counter][1] = int(values[2])
            counter += 1

    with open(path_def+"graph.def") as json_file:
        data = json.load(json_file)
	data = setName(data, "Directed Graph")
        data = setPlural(data, "Directed Graphs")

        options = dict({
	    "edges": {
	           "directed": True
		}
        })
        data = setRawTypes(data, raw_types)
        data = setAttributes(data, ["edges"])
        data = setOptions(data, options)
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        raw = dict()
        if isinstance(raw_types, list):
            for raw_type in raw_types:
                if raw_type == "dense":
                    raw["dense"] = {"edges": adj_matrix}
                if raw_type == "sparse":
                    raw["sparse"] = {"edges": graph_list}  
        else:
            if raw_types == "dense":
                raw["dense"] = {"edges": adj_matrix}
            else:
                raw["sparse"] = {"edges": graph_list}                      
        data = setRaw(data, raw)
    createOutput(raw_types, data, "Directed Graph", file_name)

		

def add_data_g(file_name, raw_types):
    file = open(PATH+file_name, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

            # to create a empty list
            graph_list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                graph_list[i] = [0] * 2
        values= []
        if each_line[0] == "e":
            #e, nv, ne, ew = each_line.split()
            values = each_line.split()

            adj_matrix[int(values[1]) - 1][int(values[2]) - 1] = 1  # upper triangular matrix
            adj_matrix[int(values[2])-1][int(values[1])-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(values[1])
            graph_list[counter][1] = int(values[2])
            counter += 1

    with open(path_def+"graph.def") as json_file:
        data = json.load(json_file)
	data = setName(data, "Graph")
        data = setPlural(data, "Graphs")
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        options = dict()
        data = setAttributes(data, ["edges"])
        data = setOptions(data, options)
        data = setRawTypes(data, raw_types)
        raw = dict()
        if isinstance(raw_types, list):
            for raw_type in raw_types:
                if raw_type == "dense":
                    raw["dense"] = {"edges": adj_matrix}
                if raw_type == "sparse":
                    raw["sparse"] = {"edges": graph_list}  
        else:
            if raw_types == "dense":
                raw["dense"] = {"edges": adj_matrix}
            else:
                raw["sparse"] = {"edges": graph_list}                      
        data = setRaw(data, raw)

    createOutput(raw_types, data, "Graph", file_name)

def createOutput(raw_types, data, graph_name, file_name):
    #Create a json file for the generated data
    json_name = PATH + file_name
    if isinstance(raw_types, list):
        for raw_type in raw_types:
            json_name += "_" + raw_type
    else:
        json_name += "_" + raw_types
    json_name += "_" + graph_name
    with open(json_name + '.json', 'w') as outfile:
        json.dump(data, outfile)

def setName(data, name):
    data["name"] = name
    return data
    
def setPlural(data, plural):
    data["plural"] = plural
    return data

def setAttributes(data, attributes):
    for default in data["attribute_types"]:
        data["attribute_types"][default] = False
    for attribute in attributes:
        data["attribute_types"][attribute] = True
    for default in data["attribute_types"]:
        if data["attribute_types"][default] == False:
            for raw_type in data["raw"]:
                del data["raw"][raw_type][default]  
    return data

def setOptions(data, options):
    for option in data["options"]:
        for s_option in data["options"][option]:
             data["options"][option][s_option] = False
    if len(options) != 0:
        for option in options:
            for sub_option in options[option]:
                data["options"][option][sub_option] = True   
    return data

def setSize(data, sizes):
    for size in sizes:
        data["size"][size] = sizes[size]
    return data

def setRaw(data, raw):
    for raw_type in raw:
        if data["raw_types"][raw_type] == True:
            for attr_raw in raw[raw_type]:     
                if data["attribute_types"][attr_raw] == True:
                    data["raw"][raw_type][attr_raw] = raw[raw_type][attr_raw]
                else:
                   del data["raw"][raw_type][attr_raw]
    return data

def setRawTypes(data, raw_types):
    for raw_type in data["raw_types"]:
        data["raw_types"][raw_type] = False
    if isinstance(raw_types, list):
        for raw_type in raw_types:
            data["raw_types"][raw_type] = True
    else:
        data["raw_types"][raw_types] = True

    for raw_type in data["raw_types"]:
         if data["raw_types"][raw_type] == False:
             del data["raw"][raw_type] 
    return data

def add_data_tulip(file_name, raw_types):
    graph = tlp.loadGraph(file_name)
    tlp.saveGraph(graph, "temp.json")
    with open("temp.json") as json_file:
        json_data = json.load(json_file)
        with open(path_def+"graph.def") as json_file_data:
            data = json.load(json_file_data)
            sizes = dict({
                "edges": int(json_data["graph"]["edgesNumber"]),
                "vertices": int(json_data["graph"]["nodesNumber"])
            })
            data = setSize(data, sizes)
            options = dict()
            edges = json_data["graph"]["edges"]
            node_weights = []
            if json_data["graph"]["properties"]["Weight"]["nodesValues"] != "":
                data = setAttributes(data, ["edges", "vertices"])
                options["vertices"] = {"weighted":"True"}
                for w in json_data["graph"]["properties"]["Weight"]["nodesValues"]:
                    node_weights.append(int(json_data["graph"]["properties"]["Weight"]["nodesValues"][w]))
            else:
                data = setAttributes(data, ["edges"])
            edge_weights = []
            if json_data["graph"]["properties"]["Weight"]["edgesValues"] != "":
                options["edges"] = {"weighted":"True"}
                for w in json_data["graph"]["properties"]["Weight"]["edgesValues"]:
                    edge_weights.append(int(json_data["graph"]["properties"]["Weight"]["edgesValues"][w]))

            data = setOptions(data, options)
            data = setRawTypes(data, raw_types)
            raw = dict()
            # to create a zero matrix
            adj_matrix = [0] * sizes["vertices"]
            for i in range(sizes["vertices"]):
                adj_matrix[i] = [0] * sizes["vertices"]

            # to create a empty list
            graph_list = [0] * sizes["edges"]
            if not edge_weights:
                list_size=2
            else:
                list_size=3
            for i in range(sizes["edges"]):
                graph_list[i] = [0] * list_size
                adj_matrix[edges[i][0]][edges[i][1]]=1
                adj_matrix[edges[i][1]][edges[i][0]]=1
                for j in range(list_size):
                    if j == 2:
                        graph_list[i][j]=edge_weights[i]
                        adj_matrix[edges[i][0]][edges[i][1]]=edge_weights[i]
                        adj_matrix[edges[i][1]][edges[i][0]]=edge_weights[i]
                    else:
                        graph_list[i][j]=edges[i][j]
            
            
            if isinstance(raw_types, list):
                for raw_type in raw_types:
                    if raw_type == "dense":
                        if node_weights:
                            raw["dense"] = {"edges": adj_matrix, "vertices": node_weights}
                        else:
                            raw["dense"] = {"edges": adj_matrix}
                    if raw_type == "sparse":
                        if node_weights:
                            raw["sparse"] = {"edges": graph_list, "vertices": node_weights}
                        else:
                            raw["sparse"] = {"edges": graph_list}
            else:
                if raw_types == "dense":
                    if node_weights:
                        raw["dense"] = {"edges": adj_matrix, "vertices": node_weights}
                    else:
                        raw["dense"] = {"edges": adj_matrix}
                else:
                    if node_weights:
                        raw["sparse"] = {"edges": graph_list, "vertices": node_weights}
                    else:
                        raw["sparse"] = {"edges": graph_list}    

            data = setRaw(data, raw)
     

            createOutput(raw_types, data, "TlpGraph", file_name)

def main(file_name):
    add_data_tulip("graphtlp.tlp", "sparse")
    '''raw_types = ["sparse", "dense"]
    for raw_type in raw_types:
        add_data_g(file_name, raw_type)
        add_data_dg(file_name, raw_type)
        #add_data_ewg(file_name, raw_type)
        #add_data_dewg(file_name, raw_type)
        add_data_vwg(file_name, raw_type)
        add_data_dvwg(file_name, raw_type)
        #add_data_evwg(file_name, raw_type)
        #add_data_devwg(file_name, raw_type)'''

'''main("GEOM20.col")
main("GEOM20a.col")
main("GEOM20b.col")

main("GEOM30.col")
main("GEOM30a.col")
main("GEOM30b.col")

main("GEOM40.col")
main("GEOM40a.col")
main("GEOM40b.col")

main("GEOM50.col")
main("GEOM50a.col")
main("GEOM50b.col")

main("GEOM60.col")
main("GEOM60a.col")
main("GEOM60b.col")

main("GEOM70.col")
main("GEOM70a.col")
main("GEOM70b.col")

main("GEOM80.col")
main("GEOM80a.col")
main("GEOM80b.col")

main("GEOM90.col")
main("GEOM90a.col")
main("GEOM90b.col")

main("GEOM100.col")
main("GEOM100a.col")
main("GEOM100b.col")

main("GEOM110.col")
main("GEOM110a.col")
main("GEOM110b.col")

main("GEOM120.col")
main("GEOM120a.col")
main("GEOM120b.col")'''

main("myciel5g.col")
'''main("myciel5gb.col")
main("myciel6g.col")
main("myciel6gb.col")
main("myciel7g.col")
main("myciel7gb.col")

main("queen8_8g.col")
main("queen8_8gb.col")

main("queen9_9g.col")
main("queen9_9gb.col")

main("queen10_10g.col")
main("queen10_10gb.col")

main("queen11_11g.col")
main("queen11_11gb.col")

main("queen12_12g.col")
main("queen12_12gb.col")

main("R50_1g.col")
main("R50_1gb.col")

main("R50_5g.col")
main("R50_5gb.col")

main("R50_9g.col")
main("R50_9gb.col")

main("R75_1g.col")
main("R75_1gb.col")

main("R75_5g.col")
main("R75_5gb.col")

main("R75_9g.col")
main("R75_9gb.col")

main("R100_1g.col")
main("R100_1gb.col")

main("R100_5g.col")
main("R100_5gb.col")

main("R100_9g.col")
main("R100_9gb.col")'''


# to try any function
