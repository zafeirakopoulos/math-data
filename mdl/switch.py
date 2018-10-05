import generic_add_data


def print_menu():
    print(25 * "-", "Math-Data", 25 * "-")

    print("1. Formal Power Series")
    print("2. Graph")
    print("3. something")
    print("4. something")
    print("5. something")
    print("6. Exit")
    print(61 * "-")


def print_graph_menu():
    print("1. Graph")
    print("2. Directed")
    print("3. Edge Weighted")
    print("4. Vertex Weighted")
    print("5. Directed, Edge Weighted")
    print("6. Directed, Vertex Weighted")
    print("7. Edge, Vertex Weighted")
    print("8. Directed, Edge and Vertex Weighted")


loop_1 = True
loop_2 = True

while loop_1:
    print_menu()
    choice = input("Enter your choice [1-5]: ")

    if choice == "1":
        continue
    elif choice == "2":
        print_graph_menu()
        choice_2 = input("Enter your choice [1-7]: ")
        if choice_2 == "1":
            filename = input("Enter the file name (for example -sample_graph.txt-) :  ")
            generic_add_data.add_data_g(filename)
        elif choice_2 == "2":
            filename = input("Enter the file name (for example -sample_graph.txt-) :  ")
            generic_add_data.add_data_dg(filename)
        elif choice_2 == "3":
            filename = input("Enter the file name (for example -sample_graph.txt-) :  ")
            generic_add_data.add_data_ewg(filename)
    elif choice == 6:
        loop_1 = False
