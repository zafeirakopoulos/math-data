
def dense_conv(file):
    file = open(file, "r")
    edge_weight = 1  # default value
    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            # print(number_nodes)
            # print(number_edges)

            # to create a zero matrix
            adj_matrix = [0] * int(number_nodes)
            for i in range(int(number_nodes)):
                adj_matrix[i] = [0] * int(number_nodes)
            # to create a zero matrix


        if each_line[0] == "e":
            # print(each_line)
            e, nv, ne = each_line.split()
            # print(nv)
            # print(ne)
            adj_matrix[int(nv)-1][int(ne)-1] = edge_weight      # upper triangular matrix
            # adj_matrix[int(ne)-1][int(nv)-1] = edge_weight    # lower triangular matrix

    print(adj_matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in adj_matrix]))  # to print matrix nicely

    return adj_matrix



dense_conv("graph_name.txt")
