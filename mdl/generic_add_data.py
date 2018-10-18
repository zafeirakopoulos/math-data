import json
import interpreter
import string

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


def create_matrix(number_nodes):
    adj_matrix = [0] * int(number_nodes)
    for i in range(int(number_nodes)):
        adj_matrix[i] = [0] * int(number_nodes)
    return adj_matrix
			

def create_list(number_edges, row_size):
    graph_list = [0] * int(number_edges)
    for i in range(int(number_edges)):
        graph_list[i] = [0] * row_size
    return graph_list
	
def create_json_file(data):
    choice = raw_input("Do you want to create a json file (y/n): ")
    if choice is "y":
        filename = raw_input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)
    else:
        raise Exception("Answer should be y or n!")

def create_raw_base(option, number_nodes, number_edges, row_size):
    if option == "d":
	     # to create a zero matrix
        raw = create_matrix(number_nodes)
    elif option == "s":
	    # to create a empty list
        raw = create_list(number_edges, row_size)
    else:
        raise Exception("The option is not found.")
    return raw

def put_option(option, data):
    if option == "d":
        data["raw_types"] = ["dense"]
        del data["raw"]["sparse"]
    if option == "s":
        data["raw_types"] = ["sparse"]
        del data["raw"]["dense"]
	return data
	
def add_data_devwg(file, dense_sparse):
    file = open(file, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            raw = create_raw_base(dense_sparse, number_nodes,  number_edges, 3)
            # for vertices
            vertices_list = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()
            if dense_sparse == "d":
                raw[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
                # raw[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix
            elif dense_sparse == "s":
                raw[counter][0] = int(nv)
                raw[counter][1] = int(ne)
                raw[counter][2] = int(ew)
            else:
			    raise Exception("Option is not found.")
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)

    data = interpreter.interpret("Directed Vertex and Edge Weighted Graph")
    data["features"]["directed"] = "True"
    print(data)
    data["raw"]["dense"]["edges"] = raw
    print(data)
    if dense_sparse == "d":
        data["raw"]["dense"]["vertices"] = vertices_list
    data = put_option(dense_sparse, data)
    print(data)
    create_json_file(data)

def add_data_evwg(file, dense_sparse):
    file = open(file, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            raw = create_raw_base(dense_sparse, number_nodes,  number_edges, 3)
            # for vertices
            vertices_list = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()
            if dense_sparse == "d":
                raw[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
                # raw[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix
            elif dense_sparse == "s":
                raw[counter][0] = int(nv)
                raw[counter][1] = int(ne)
                raw[counter][2] = int(ew)
            else:
			    raise Exception("Option is not found.")
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)

    data = interpreter.interpret("Vertex and Edge Weighted Graph")
    data["raw"]["dense"]["edges"] = raw
    if dense_sparse == "d":
        data["raw"]["dense"]["vertices"] = vertices_list
    data = put_option(dense_sparse, data)
    create_json_file(data)

def add_data_dvwg(file, dense_sparse):
    file = open(file, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            raw = create_raw_base(dense_sparse, number_nodes, number_edges, 2)

            # for vertices
            vertices_list = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()
            if dense_sparse == "d":
                raw[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
                # raw[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix
            elif dense_sparse == "s":
                raw[counter][0] = int(nv)
                raw[counter][1] = int(ne)
            else:
			    raise Exception("Option is not found.")
            counter += 1

        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)

    data = interpreter.interpret("Directed Vertex Weighted Graph")
    data["features"]["directed"] = "True"
    data["raw"]["dense"]["edges"] = raw
    data["raw"]["sparse"]["vertices"] = vertices_list
    data = put_option(dense_sparse, data)
    create_json_file(data)

def add_data_dewg(file, dense_sparse):
    file = open(file, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            raw = create_raw_base(dense_sparse, number_nodes, number_edges, 3)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()
            if dense_sparse == "d":
                raw[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
                # raw[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix
            elif dense_sparse == "s":
                raw[counter][0] = int(nv)
                raw[counter][1] = int(ne)
                raw[counter][2] = int(ew)
            else:
			    raise Exception("Option is not found.")
            counter += 1

    data = interpreter.interpret("Directed Edge Weighted Graph")
    data["features"]["directed"] = "True"
    data["raw"]["dense"]["edges"] = raw
    data = put_option(dense_sparse, data)
    create_json_file(data)

def add_data_vwg(file, dense_sparse):
    file = open(file, "r")
    counter = 0  # to create list properly
    raw = []
    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            raw = create_raw_base(dense_sparse, number_nodes, number_edges, 2)
            print(raw)
            # for vertices
            vertices_list = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()
            
            if dense_sparse == "d":
                raw[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
                # raw[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix
            elif dense_sparse == "s":
                raw[counter][0] = int(nv)
                raw[counter][1] = int(ne)
            else:
			    raise Exception("Option is not found.")
            counter += 1
        if each_line[0] == "n":
            n, nn, vw = each_line.split()
            vertices_list[int(nn) - 1] = int(vw)	
    data = interpreter.interpret("Vertex Weighted Graph")
    data["raw"]["dense"]["vertices"] = vertices_list
    data["raw"]["dense"]["edges"] = raw
    data = put_option(dense_sparse, data)
    print(data)
    #create_json_file(data)
    choice = raw_input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = raw_input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_ewg(file, dense_sparse):
    file = open(file, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            raw = create_raw_base(dense_sparse, number_nodes, number_edges, 3)

        if each_line[0] == "e":
            e, nv, ne, ew = each_line.split()
            if dense_sparse == "d":
                raw[int(nv) - 1][int(ne) - 1] = int(ew)  # upper triangular matrix
                # raw[int(ne)-1][int(nv)-1] = int(ew)    # lower triangular matrix
            elif dense_sparse == "s":
                raw[counter][0] = int(nv)
                raw[counter][1] = int(ne)
                raw[counter][2] = int(ew)
            else:
			    raise Exception("Option is not found.")
            counter += 1

    data = interpreter.interpret("Edge Weighted Graph")
    data["raw"]["dense"]["edges"] = raw
    data = put_option(dense_sparse, data)
    create_json_file(data)
	
def add_data_dg(file, dense_sparse):
    file = open(file, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            raw = create_raw_base(dense_sparse, number_nodes, number_edges, 2)

        if each_line[0] == "e":
            e, nv, ne = each_line.split()
            if dense_sparse == "d":
                raw[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
                # raw[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix
            elif dense_sparse == "s":
                raw[counter][0] = int(nv)
                raw[counter][1] = int(ne)
            else:
			    raise Exception("Option is not found.")
            counter += 1

    data = interpreter.interpret("Directed Graph")
    data["features"]["directed"] = "True"
    data["raw"]["dense"]["edges"] = raw
    data = put_option(dense_sparse, data)
    create_json_file(data)


def add_data_g(file, dense_sparse):
    file = open(file, "r")
    counter = 0  # to create list properly

    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            raw = create_raw_base(dense_sparse, number_nodes, number_edges, 2)

        if each_line[0] == "e":
            e, nv, ne = each_line.split()
            if dense_sparse == "d":
                raw[int(nv) - 1][int(ne) - 1] = 1  # upper triangular matrix
                # raw[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix
            elif dense_sparse == "s":
                raw[counter][0] = int(nv)
                raw[counter][1] = int(ne)
            else:
			    raise Exception("option is not found")
            counter += 1
    data = interpreter.interpret("Graph")
    data["raw"]["dense"]["edges"] = raw
    data = put_option(dense_sparse, data)
    create_json_file(data)