import sys

temp = sys.path[0]
newpath = sys.path[0]
newpath = newpath[:-5]
newpath = newpath + "\\core\\db"
sys.path[0] = newpath

from io import MDB
from db import DB, Table

sys.path[0] = temp
import os
import json


def test_add_instance():

    r = {
        "raw": "something",
        "features": "something",
        "semantics": "something",
        "context": 'list',
        "typeset": "something",
        "commit": "commit-message"
    }

    response = MDB.add_instance(data, r)
    print(response)
    return response


def test_remove_instance(sha):

    r = {
        "sha": sha,
        "commit" : "removed"
    }

    response = io.remove_instance(data, r)
    print(response)
    return response


def test_update_instance(sha):

    r = {
        "sha": sha,
        "raw": "updated",
        "features": "updated",
        "semantics": "updated",
        "context":  "graph",
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

    data = DB("data")

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
