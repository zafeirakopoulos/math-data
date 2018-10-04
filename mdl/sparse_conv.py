

def sparse_conv(file):
    file = open(file, "r")
    counter = 0           # to create list properly
    for each_line in file.readlines():
        if each_line[0] == "p":
            p, name, number_nodes, number_edges = each_line.split()
            # print(number_nodes)
            # print(number_edges)

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



sparse_conv("graph_name.txt")