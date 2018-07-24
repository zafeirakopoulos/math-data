from mathdatabase import manage, search, io
import os
import json


def test_add_instance():

    r = {
        "datatype": "graph",
        "index": "something-"+str(file_num),
        "raw": "something-"+str(file_num),
        "features": "something-"+str(file_num),
        "semantics": "something-"+str(file_num),
        "context":  {"edge": {"1": file_num, "2": file_num},
                     "vertex": [{"first": file_num, "second": file_num},
                                {"first": file_num, "second": file_num}]},
        "typeset": "something-"+str(file_num),
        "commit": "something-"+str(file_num)
    }

    response = io.add_instance(data, r)
    print(response)
    return response


def test_remove_instance(sha):

    r = {
        "datatype": "graph",
        "sha": sha
    }

    response = io.remove_instance(data, r)
    print(response)
    return response


def test_update_instance(sha):

    r = {
        "datatype": "graph",
        "sha": sha,
        "index": "updated",
        "raw": "updated",
        "features": "updated",
        "semantics": "updated",
        "context":  {"edge": {"1": 99, "2": 2000},
                     "vertex": [{"first": 0, "second": 99},
                                {"first": 0, "second": 99}]},
        "typeset": "updated",
        "commit": "updated_repo"
    }

    response = io.update_instance(data, r)
    print(response)


def test_retrieve_instance(sha):

    r = {
        "datatype": "graph",
        "sha": sha
    }

    response = io.retrieve_instance(data, r)
    print(response)
    return response


def test_statistics():

    return data.statistics()


def test_find(text):

    r = {
        "datatype": "graph",
        "text": text
    }

    response = search.find(data, r)
    print(response)


if __name__ == "__main__":

    datatypes = ["graph"]
    path = "."

    data = manage.mdb(datatypes=datatypes, path=path)

    with open(os.path.join(path, "log.txt")) as json_file:
        dic = json.load(json_file)

    total = dic["remaining-graph"]

    file_num = dic["graph"] + 1

    print("------  OPERATIONS    ------")
    print("------  1. add        ------")
    print("------  2. remove     ------")
    print("------  3. update     ------")
    print("------  4. retrieve   ------")
    print("------  5. statistics ------")
    print("------  6. find       ------")
    print("------ -1. exit       ------")

    operation = input("Which operation do you want : ")

    while operation != "-1":
        while not operation.isdigit():
            print("Please enter a digit which are represented as table!")
            operation = input("Which operation do you want : ")

        if operation == "1":
            # add operation
            test_add_instance()

        elif operation == "2":

            if total == 0:
                print("Before remove operation we add a new data type")
            else:
                # remove operation
                test_remove_instance(input("Enter sha key : "))
                total -= 1
        elif operation == "3":

            if total == 0:
                print("Before update operation we add a new data type")
            else:
                # update operation
                test_update_instance(input("Enter sha key : "))
        elif operation == "4":
            if total == 0:
                print("Before retrieve operation we add a new data type")
            else:
                # operation operation
                test_retrieve_instance(input("Enter sha key : "))
        elif operation == "5":
            print(test_statistics())

        elif operation == "6":
            if total == 0:
                print("Before find operation we add a new data type")
            else:
                test_find(input("What do you want to find: "))
        else:
            print(operation, "is not supported!")

        operation = input("Which operation do you want : ")

    print("Exited from the test!")
