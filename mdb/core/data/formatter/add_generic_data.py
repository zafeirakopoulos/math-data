import json
import string
import os
import sys
import collections
new_path = sys.path[0]
print(new_path)
new_path = new_path[:-10] + "/language/"
sys.path[0] = new_path
print(sys.path[0])
path_def = new_path[:-24] + "/local/defs/"
new_path = new_path[:-24] + "/local/third_party/"
PATH = new_path   #should be changed



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

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
            #adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            graph_list[counter][2] = int(ew)
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)
		
    with open(path_def+"general_graph.def") as json_file:
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
        if isinstance(raw_types, list):
            for raw_type in range(len(raw_types)):
                print(raw_types[raw_type])
                options["raw_types"] = {raw_type: True}
        else:
           options["raw_types"] = {raw_types: True}

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

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
            adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            graph_list[counter][2] = int(ew)
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)
		
    with open(path_def+"general_graph.def") as json_file:
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

        if isinstance(raw_types, list):
            for raw_type in range(len(raw_types)):
                print(raw_types[raw_type])
                options["raw_types"] = {raw_type: True}
        else:
           options["raw_types"] = {raw_types: True}


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

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
            #adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)
		
    with open(path_def+"general_graph.def") as json_file:
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
        if isinstance(raw_types, list):
            for raw_type in range(len(raw_types)):
                print(raw_types[raw_type])
                options["raw_types"] = {raw_type: True}
        else:
           options["raw_types"] = {raw_types: True}


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

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
            #adj_matrix[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            graph_list[counter][2] = int(ew)
            counter += 1

    with open(path_def+"general_graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Directed Edge Weighted Graph")
        data = setPlural(data, "Directed Edge Weighted Graphs")
        options = dict({
			"edges": {
			           "weighted": True,
			           "directed": True
			}
        })
        if isinstance(raw_types, list):
            for raw_type in range(len(raw_types)):
                print(raw_types[raw_type])
                options["raw_types"] = {raw_type: True}
        else:
           options["raw_types"] = {raw_types: True}

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

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
            adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)
		
    with open(path_def+"general_graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Vertex Weighted Graph")
        data = setPlural(data, "Vertex Weighted Graphs")
        options = dict({
			"vertices": {
			           "weighted": True
			}
        })
        if isinstance(raw_types, list):
            for raw_type in range(len(raw_types)):
                print(raw_types[raw_type])
                options["raw_types"] = {raw_type: True}
        else:
           options["raw_types"] = {raw_types: True}

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

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
            adj_matrix[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            graph_list[counter][2] = int(ew)
            counter += 1

    with open(path_def+"general_graph.def") as json_file:
        data = json.load(json_file)
        data = setName(data, "Edge Weighted Graph")
        data = setPlural(data, "Edge Weighted Graphs")
        options = dict({

		"edges": {
		           "weighted": True
			}
        })
        if isinstance(raw_types, list):
            for raw_type in range(len(raw_types)):
                print(raw_types[raw_type])
                options["raw_types"] = {raw_type: True}
        else:
           options["raw_types"] = {raw_types: True}


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

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
            #adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            counter += 1

    with open(path_def+"general_graph.def") as json_file:
        data = json.load(json_file)
	data = setName(data, "Directed Graph")
        data = setPlural(data, "Directed Graphs")

        options = dict({
	    "edges": {
	           "directed": True
		}
        })
        if isinstance(raw_types, list):
            for raw_type in range(len(raw_types)):
                print(raw_types[raw_type])
                options["raw_types"] = {raw_type: True}
        else:
           options["raw_types"] = {raw_types: True}


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

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
            adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            counter += 1

    with open(path_def+"general_graph.def") as json_file:
        data = json.load(json_file)
	data = setName(data, "Graph")
        data = setPlural(data, "Graphs")
        options = dict()
        if isinstance(raw_types, list):
            for raw_type in range(len(raw_types)):
                print(raw_types[raw_type])
                options["raw_types"] = {raw_type: True}
        else:
            options["raw_types"] = {raw_types: True}


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
    for default in data["attributes"]:
        data["attributes"][default] = False
    for attribute in attributes:
        data["attributes"][attribute] = True
    for default in data["attributes"]:
        if data["attributes"][default] == False:
            for raw_type in data["raw"]:
                del data["raw"][raw_type][default]  
    return data

def setOptions(data, options):
    for option in data["options"]:
        for s_option in data["options"][option]:
             data["options"][option][s_option] = False
    for option in options:
         for sub_option in options[option]:
            data["options"][option][sub_option] = True
    for s_option in data["options"]["raw_types"]:
         if data["options"]["raw_types"][s_option] == False:
             del data["raw"][s_option]    
    return data

def setSize(data, sizes):
    for size in sizes:
        data["size"][size] = sizes[size]
    return data

def setRaw(data, raw):
    for raw_type in raw:
        if data["options"]["raw_types"][raw_type] == True:
            for attr_raw in raw[raw_type]:     
                if data["attributes"][attr_raw] == True:
                    data["raw"][raw_type][attr_raw] = raw[raw_type][attr_raw]
                else:
                   print(data["raw"][raw_type][attr_raw])
                   del data["raw"][raw_type][attr_raw]
    return data

def main(file_name):
    raw_types = ["sparse", "dense"]
    for raw_type in raw_types:
        add_data_g(file_name, raw_type)
        add_data_dg(file_name, raw_type)
        add_data_ewg(file_name, raw_type)
        add_data_dewg(file_name, raw_type)
        add_data_vwg(file_name, raw_type)
        add_data_dvwg(file_name, raw_type)
        add_data_evwg(file_name, raw_type)
        add_data_devwg(file_name, raw_type)

#main("GEOM20.col")
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
main("GEOM120b.col")



# to try any function
