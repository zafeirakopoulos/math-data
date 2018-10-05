import json


def dense_conv(file):
    file = open(file, "r")
    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)

        if each_line[0] == "e":
            e, nv, ne = each_line.split()

            adj_matrix[int(nv)-1][int(ne)-1] = 1      # upper triangular matrix
            # adj_matrix[int(ne)-1][int(nv)-1] = 1    # lower triangular matrix

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely

    return adj_matrix

def sparse_conv(file):
    file = open(file, "r")
    counter = 0           # to create list properly
    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()

            # to create a empty list
            list = [0] * int(number_edges)
            for i in range(int(number_edges)):
                list[i] = [0] * 2

        if each_line[0] == "e":
            e, nv, ne = each_line.split()
            list[counter][0] = nv
            list[counter][1] = ne
            counter += 1
    print(list)

    return list

with open ("graph.def") as json_file:
    data = json.load(json_file)
    data["raw"]["dense"]["edges"] = dense_conv("sample_graph.txt")
    data["raw"]["sparse"]["edges"] = sparse_conv("sample_graph.txt")
    print(data)
    with open('new_graph.json', 'w') as outfile:
        json.dump(data, outfile)