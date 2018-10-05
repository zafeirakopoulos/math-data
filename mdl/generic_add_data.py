import json
import interpreter


def add_data_ewg(file):
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

            graph_list[counter][0] = nv
            graph_list[counter][1] = ne
            counter += 1

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Edge Weighted Graph")
    data["raw"]["dense"]["edges"] = adj_matrix
    data["raw"]["sparse"]["edges"] = graph_list
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_dg(file):
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

            graph_list[counter][0] = nv
            graph_list[counter][1] = ne
            counter += 1

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    data = interpreter.interpret("Directed Graph")
    data["features"]["directed"] = "True"
    data["raw"]["dense"]["edges"] = adj_matrix
    data["raw"]["sparse"]["edges"] = graph_list
    print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)


def add_data_g(file):
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

            graph_list[counter][0] = nv
            graph_list[counter][1] = ne
            counter += 1

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely
    print(graph_list)

    with open("graph.def") as json_file:
        data = json.load(json_file)
        data["raw"]["dense"]["edges"] = adj_matrix
        data["raw"]["sparse"]["edges"] = graph_list
        print(data)
    choice = input("Do you want to create a json file (y/n): ")
    if choice == "y":
        filename = input("Enter the file name : ")
        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile)
