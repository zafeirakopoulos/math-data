import json
import interpreter


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


def add_data_g(file, dense_sparse):
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

    with open("graph.def") as json_file:
        data = json.load(json_file)
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


# to try any function
#add_data_g("edge_vertex.txt", "d")
