from mdbutil.db import DB

if __name__ == '__main__':
    db = DB("db")

    print("------    OPERATIONS       ------")
    print("------    1. add           ------")
    print("------    2. remove        ------")
    print("------    3. update        ------")
    print("------    4. retrieve      ------")
    print("------    5. list files    ------")
    print("------    -1. exit         ------")

    operation = input("Which operation do you want : ")

    while operation != "-1":
        while not operation.isdigit():
            print("Please enter a digit which are represented as table!")
            operation = input("Which operation do you want : ")

        if operation == "1":
            path = input("Please enter file path:")
            msg = input("Please enter commit message:")

            if path is "":
                path = "test_file1.json"
            if msg is "":
                msg = "this is a test"

            print(db['test'].add(path, msg))
        elif operation == "2":
            sha = input("Please enter commit SHA:")

            db['test'].remove(sha)
        elif operation == "3":
            sha = input("Please enter commit SHA:")
            content = input("Please enter new content:")
            msg = input("Please enter commit message:")

            if msg is "":
                msg = "another test"

            print(db['test'].update(sha, content, msg))
        elif operation == "4":
            sha = input("Please enter commit SHA:")

            result = db['test'][sha]
            if result is not None:
                for filename, content in result:
                    print("=====%s" % filename)
                    print(content.read())
        elif operation == "5":
            for entry in db['test']:
                print(entry)

        else:
            print("not a valid entry")

        operation = input("Which operation do you want : ")

    print("Exited from the test!")
