from math_data import math_data
import os
import shutil


def test_add_instance():

    r = {
        "datatype": "graph",
        "index": "yeni...",
        "raw": "something...",
        "features": "something...",
        "semantics": "something...",
        "context":  {"edge": {"1": 1, "2": 2},
                     "vertex": [{"first": 2, "second": 1},
                                {"first": 23, "second": 55}]},
        "typeset": "something...",
        "commit": "something..."
    }

    response = data.add_instance(r)
    print(response)
    return response


def test_remove_instance(sha):

    r = {
        "datatype": "graph",
        "sha": sha
    }

    response = data.remove_instance(r)
    print(response)
    return response


def test_update_instance(sha):

    r = {
        "datatype": "graph",
        "sha": sha,
        "index": "second test",
        "raw": "something...",
        "features": "safdfsdg",
        "semantics": "something...",
        "context":  {"edge": {"1": 100, "2": 2000},
                     "vertex": [{"first": 4, "second": 4},
                                {"first": 3, "second": 55}]},
        "typeset": "something...",
        "commit": "update_repo"
    }

    response = data.update_instance(r)
    print(response)


def test_retrieve_instance(sha):

    r = {
        "datatype": "graph",
        "sha": sha,

    }

    response = data.retrieve_instance(r)
    print(response)
    return response


if __name__ == "__main__":

    datatypes = ["graph"]
    path = "."

    # preparation to sample
    # removing old data types
    for datatype in datatypes:
        dir_datatype = os.path.join(path, datatype)

        if os.path.exists(dir_datatype):
            shutil.rmtree(dir_datatype, ignore_errors=True)
            os.remove(os.path.join(path, "log.txt"))

    data = math_data(datatypes=datatypes, path=path)

    print("------  OPERATIONS  ------")
    print("------  1. add      ------")
    print("------  2. remove   ------")
    print("------  3. update   ------")
    print("------  4. retrieve ------")
    print("------ -1. exit     ------")

    operation = input("Which operation do you want : ")

    while operation != "-1":
        while not operation.isdigit():
            print("Please enter a digit which are represented as table!")
            operation = input("Which operation do you want : ")

        if operation == "1":
            # add operation
            test_add_instance()

        elif operation == "2":

            print("Before remove operation we add a new data type")
            sha = test_add_instance()

            # remove operation
            test_remove_instance(sha["sha"])
        elif operation == "3":

            print("Before update operation we add a new data type")
            sha = test_add_instance()

            # update operation
            test_update_instance(sha["sha"])
        elif operation == "4":

            print("Before retrieve operation we add a new data type")
            sha = test_add_instance()

            # operation operation
            test_retrieve_instance(sha["sha"])
        else:
            print(operation, "is not supported!")

        operation = input("Which operation do you want : ")

    print("Exited from the test!")
