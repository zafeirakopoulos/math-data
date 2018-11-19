import json
import string
import os
import sys
new_path = sys.path[0]
print(new_path)
new_path = new_path[:-10] + "/language/"
sys.path[0] = new_path
print(sys.path[0])
import interpreter
path_def = new_path[:-24] + "/local/defs/"
new_path = new_path[:-24] + "/local/third_party/"
PATH = new_path   #should be changed
#C:\Users\Hakan\Desktop\Proje\math-data\local\third_party


def add_data_polytope(file, raw_type):
    file = open(file, "r")
    cnt_1 = 0

    for each_line in file.readlines():
        if "INEQUALITIES" in each_line or cnt_1 != 0:
            print("okay")
            if "INEQUALITIES" in each_line:
                matrix = [0] * 7
                for i in range(7):
                    matrix[i] = [0] * 2
                    matrix[i][0] = [0, 0, 0]
                print(matrix)

            if "<v>" in each_line:
                each_line.replace("<v>", "")
                each_line.replace("</v>", "")
                print(each_line)
                b, a1, a2, a3 = each_line.split()
                print(a1)
                matrix[cnt_1][0][0] = int(a1)
                matrix[cnt_1][0][1] = int(a2)
                matrix[cnt_1][0][2] = int(a3)
                matrix[cnt_1][1] = int(b)

            if "</m>" in each_line:
                cnt_1 = 0
            else:
                cnt_1 = cnt_1 + 1



def add_data_devwg(file, dense_sparse):
    file = open(file, "r")
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

            # for vertices
            vertices_list = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
            # adj_matrix[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            graph_list[counter][2] = int(ew)
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Directed Vertex and Edge Weighted Graph")
    data["features"]["directed"] = "True"
    if dense_sparse == "d":
        data["raw"]["dense"]["vertices"] = vertices_list
        data["raw"]["dense"]["edges"] = adj_matrix
        data["raw_types"] = ["dense"]
        del data["raw"]["sparse"]
    if dense_sparse == "s":
        data["raw"]["sparse"]["edges"] = graph_list
        data["raw_types"] = ["sparse"]
        del data["raw"]["dense"]
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_evwg(file, dense_sparse):
    file = open(file, "r")
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

            # for vertices
            vertices_list = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
            # adj_matrix[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            graph_list[counter][2] = int(ew)
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Vertex and Edge Weighted Graph")
    if dense_sparse == "d":
        data["raw"]["dense"]["vertices"] = vertices_list
        data["raw"]["dense"]["edges"] = adj_matrix
        data["raw_types"] = ["dense"]
        del data["raw"]["sparse"]
    if dense_sparse == "s":
        data["raw"]["sparse"]["edges"] = graph_list
        data["raw_types"] = ["sparse"]
        del data["raw"]["dense"]
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_dvwg(file, dense_sparse):
    file = open(file, "r")
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

            # for vertices
            vertices_list = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
            # adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Directed Vertex Weighted Graph")
    data["features"]["directed"] = "True"
    if dense_sparse == "d":
        data["raw"]["dense"]["vertices"] = vertices_list
        data["raw"]["dense"]["edges"] = adj_matrix
        data["raw_types"] = ["dense"]
        del data["raw"]["sparse"]
    elif dense_sparse == "s":
        data["raw"]["sparse"]["vertices"] = vertices_list
        data["raw"]["sparse"]["edges"] = graph_list
        data["raw_types"] = ["sparse"]
        del data["raw"]["dense"]
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_dewg(file, dense_sparse):
    file = open(file, "r")
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
            # adj_matrix[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            graph_list[counter][2] = int(ew)
            counter += 1

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Directed Edge Weighted Graph")
    data["features"]["directed"] = "True"
    if dense_sparse == "d":
        data["raw"]["dense"]["edges"] = adj_matrix
        data["raw_types"] = ["dense"]
        del data["raw"]["sparse"]
    if dense_sparse == "s":
        data["raw"]["sparse"]["edges"] = graph_list
        data["raw_types"] = ["sparse"]
        del data["raw"]["dense"]
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_vwg(file, dense_sparse):
    file = open(file, "r")
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

            # for vertices
            vertices_list = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
            # adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Vertex Weighted Graph")
    if dense_sparse == "d":
        data["raw"]["dense"]["vertices"] = vertices_list
        data["raw"]["dense"]["edges"] = adj_matrix
        data["raw_types"] = ["dense"]
        del data["raw"]["sparse"]
    elif dense_sparse == "s":
        data["raw"]["sparse"]["vertices"] = vertices_list
        data["raw"]["sparse"]["edges"] = graph_list
        data["raw_types"] = ["sparse"]
        del data["raw"]["dense"]
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_ewg(file, dense_sparse):
    file = open(file, "r")
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
            # adj_matrix[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            graph_list[counter][2] = int(ew)
            counter += 1

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Edge Weighted Graph")
    if dense_sparse == "d":
        data["raw"]["dense"]["edges"] = adj_matrix
        data["raw_types"] = ["dense"]
        del data["raw"]["sparse"]
    if dense_sparse == "s":
        data["raw"]["sparse"]["edges"] = graph_list
        data["raw_types"] = ["sparse"]
        del data["raw"]["dense"]
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_dg(file, dense_sparse):
    file = open(file, "r")
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
            e, nv, ne = each_line.split()

            adj_matrix[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
            # adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

            graph_list[counter][0] = int(nv)
            graph_list[counter][1] = int(ne)
            counter += 1

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Directed Graph")
    data["features"]["directed"] = "True"
    if dense_sparse == "d":
        data["raw"]["dense"]["edges"] = adj_matrix
        data["raw_types"] = ["dense"]
        del data["raw"]["sparse"]
    elif dense_sparse == "s":
        data["raw"]["sparse"]["edges"] = graph_list
        data["raw_types"] = ["sparse"]
        del data["raw"]["dense"]
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


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
        options = dict({
            "raw_types": raw_types
        })

        data = setAttributes(data, ["edges"])
        data = setOptions(data, options)
        sizes = dict({
            "edges": int(number_edges),
            "vertices": int(number_nodes)
        })
        data = setSize(data, sizes)
        raw = dict()
        for raw_type in raw_types:
            if raw_type == "dense":
                raw["dense"] = {"edges": adj_matrix}
            if raw_type == "sparse":
                raw["sparse"] = {"edges": graph_list} 
        print(raw)           
        data = setRaw(data, raw)
        print(data)
    #Create a json file for the generated data
    json_name = PATH + file_name
    for raw_type in raw_types:
        json_name += "_" + raw_type
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
        if isinstance(options[option], list):
            for sub_option in options[option]:
                data["options"][option][sub_option] = True
        else:
            data["options"][option] = True
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
add_data_g("GEOM20.col", ["dense", "sparse"])
# to try any function
