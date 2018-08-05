from database import manage, search, io
import os
import json


def test_add_instance():

    r = {
        "raw": "something-"+str(data.next_file["raw"]),
        "features": "something-"+str(data.next_file["features"]),
        "semantics": "something-"+str(data.next_file["semantics"]),
        "context": 'list',
        "typeset": "something-"+str(data.next_file["typeset"]),
        "commit": "commit-message-" + str(data.next_file["typeset"])
    }

    response = io.add_instance(data, r)
    print(response)
    return response


def test_remove_instance(sha):

    r = {
        "sha": sha
    }

    response = io.remove_instance(data, r)
    print(response)
    return response


def test_update_instance(sha):

    r = {
        "datatype": "graph",
        "sha": sha,
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

    basedir = os.path.join(os.getcwd(), "data")

    data = manage.mdb(basedir=basedir)

    total = 9999

    file_num = 1

    print("------    OPERATIONS       ------")
    print("------    1. add           ------")
    print("------    2. remove        ------")
    print("------    3. update        ------")
    print("------    4. retrieve      ------")
    print("------    5. statistics    ------")
    print("------    6. find          ------")
    print("------    -1. exit         ------")

    operation = input("Which operation do you want : ")

    while operation != "-1":
        while not operation.isdigit():
            print("Please enter a digit which are represented as table!")
            operation = input("Which operation do you want : ")

        if operation == "1":
            total += 1
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
