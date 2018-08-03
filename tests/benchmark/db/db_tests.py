from mdbutil.benchmark.db import DB
from uuid import uuid4
from io import TextIOWrapper

if __name__ == '__main__':
    db = DB("db")

    print("------    OPERATIONS       ------")
    print("------    1. add           ------")
    print("------    2. remove        ------")
    print("------    3. update        ------")
    print("------    4. retrieve      ------")
    print("------    -1. exit         ------")

    operation = input("Which operation do you want : ")

    while operation != "-1":
        while not operation.isdigit():
            print("Please enter a digit which are represented as table!")
            operation = input("Which operation do you want : ")

        if operation == "1":
            path = input("Please enter file path:")

            if path is "":
                path = "test_file1.json"

            print(db['test'].add(path, "this is a test"))
        elif operation == "2":
            print("not implemented")
        elif operation == "3":
            sha = input("Please enter commit SHA:")
            content = input("Please enter new content:")

            print(db['test'].update(sha, content, "another test"))
        elif operation == "4":
            sha = input("Please enter commit SHA:")

            print(db['test'][sha])
        else:
            print("not a valid entry")

        operation = input("Which operation do you want : ")

    print("Exited from the test!")
