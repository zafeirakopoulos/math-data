from threading import Lock
import os
import json
from git import Repo

mutex = Lock()


def __add_helper(mdb, data):
    """ Private Helper Function.
    Go through target path and creates new data type
    :param data: incoming json file.
    :param sha_list: sha list of all attribute such as context
    :return: none
    """

    sha_dic = {}

    if not os.path.exists(mdb.basedir):
        return "Base directory are not found", 0

    for aspect in mdb.aspects:
        # check if aspect exist

        filename = str(mdb.next_file[aspect]) + ".txt"

        mdb.next_file[aspect] += 1

        repo_path = os.path.join(mdb.basedir, aspect, mdb.current_repos[aspect])

        file_path = os.path.join(mdb.basedir, aspect, mdb.current_repos[aspect], filename)

        with open(file_path, 'w') as outfile:
            json.dump(data[aspect], outfile)

        mdb.git_add(repo_path, filename, data["commit"])

        sha_dic[aspect] = mdb.get_last_sha(repo_path, filename)

    # Instance part

    instance_file_path = os.path.join(mdb.basedir, "instance", mdb.instance_repo, "1.txt")
    instance_repo_path = os.path.join(mdb.basedir, "instance", mdb.instance_repo)
    with open(instance_file_path, "r") as json_file:
        sha_list = json.load(json_file)

    sha_list.append(sha_dic)

    mdb.git_add(instance_repo_path, "1.txt", data["commit"])

    with open(os.path.join(instance_file_path), 'w') as outfile:
        json.dump(sha_list, outfile)

    # Index part

    index_sha = mdb.get_last_sha(instance_repo_path, "1.txt")

    index_repo_path = os.path.join(mdb.basedir, "index")
    index_file_path = os.path.join(mdb.basedir, "index", "1.txt")

    with open(index_file_path, "r") as json_file:
        index_list = json.load(json_file)

    index_list.append({"sha": index_sha,
                       "repo": mdb.instance_repo})

    with open(os.path.join(index_file_path), 'w') as outfile:
        json.dump(index_list, outfile)

    status = "True"

    return status, index_sha


def add_instance(mdb, data):
    """
    It is dependent to name of data type.
    if new data type required to add new file structure is created.
    Otherwise, add just a new file.

    input example;
        r = {
            "datatype": "graph",   # may be polynomial
            "raw": "raw example",
            "features": "features example",
            "semantics": "semantics example",
            "context":  {"edge": {"1": 100, "2": 2000},
                         "vertex": [{"first": 4, "second": 4},
                                    {"first": 3, "second": 55}]},
            "typeset": "typeset example",
            "commit": "update_repo"
        }
    return example;

        {sha : a63813d76910623f2b92ca7343682fe9ee2230a1 , 'status': 1}
        if removal is unsuccessful;
        {'status': 0} # this line will be rewrite

    :param data: incoming json file.
    :return: sha key of index of datatype.
    """

    mutex.acquire()
    try:
        status, index_sha = __add_helper(mdb, data)
    finally:
        mutex.release()

    response = {
        "sha": index_sha,    # index represent all of datatype to perform on it.
        "status": status                            # if successful otherwise 0
    }
    
    return response


def remove_instance(mdb, data):
    """
    It is dependent to name of data type and its sha key.
    An example as fallow;

    input example;

        r = {
            "datatype": "graph",
            "sha": "a9f870b98077b86f4cff2afbb90c3255c8f9a923"
        }

        other example

        r = {
            "datatype": "polynomial",
            "sha": "12b8a0b98077b86f4cff2afbb90c3255c8f9affc"
        }

    return example;

        {'status': 1}

        if removal is unsuccessful;

        {'status': 0}

    :param data: incoming json file.
    :return: control status
    """
    status = 0
    datatype = data["datatype"]

    if os.path.exists(datatype):

        input_sha = data["sha"]

        dir_index = os.path.join(mdb.get_basedir(), datatype, "index")

        for filename in os.listdir(dir_index):

            # we ignore .git file
            if filename == ".git":
                continue

            if input_sha == mdb.get_first_sha(dir_index, filename):

                for attribute in mdb.get_attributes():

                    path = os.path.join(mdb.get_basedir(), datatype, attribute)

                    mdb.git_remove(path, filename, "deleted repo")

                status = 1

                # decrease log file data type and write to log again
                mdb.get_file_number()["remaining-" + datatype] -= 1
                with open(os.path.join(mdb.get_basedir(), "log.txt"), 'w') as outfile:
                    json.dump(mdb.get_file_number(), outfile)

                break

    response = {
        "status": status  # if successful otherwise 0
    }

    return response


def retrieve_instance(mdb, data):

    """ Fetches an instance which match with "input" sha key

    input example;

        r = {
            "datatype": "graph",
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

        other example

        r = {
            "datatype": "polynomial",
            "sha": "21fa767a68101f4b7e75ffe50001954d0ee37a74"
        }

    return example;

        r = {
            "datatype": "graph",   # may be polynomial
            "raw": "raw example",
            "features": "features example",
            "semantics": "semantics example",
            "context":  {"edge": {"1": 100, "2": 2000},
                         "vertex": [{"first": 4, "second": 4},
                                    {"first": 3, "second": 55}]},
            "typeset": "typeset example"
        }

    :param data: incoming json file.
    :return: desired instance
    """

    datatype = data["datatype"]

    response = {"datatype": datatype}

    status = -1

    if not os.path.exists(datatype):
        status = 0

    else:
        input_sha = data["sha"]

        dir_index = os.path.join(mdb.get_basedir(), datatype, "index")

        for filename in os.listdir(dir_index):

            if filename == ".git":
                continue

            if input_sha == mdb.get_first_sha(dir_index, filename):
                for attribute in mdb.get_attributes():
                    file_path = os.path.join(mdb.get_basedir(), datatype, attribute, filename)

                    with open(file_path, "r") as json_file:
                        response[attribute] = json.load(json_file)

                status = 1
                break

    response["status"] = status

    return response


def __update_file(mdb, content, path, commit_message, filename):

    """Private Helper Function.
    Write new data to target file. Add repository with new commit message
    :param content: New content to edit target file
    :param path: repository path
    :param commit_message:
    :param filename:
    :return: none
    """


    # generate path
    file_path = os.path.join(path, filename)

    # write target file
    with open(file_path, 'w') as outfile:
        json.dump(content, outfile)

    mdb.git_add(path, filename, commit_message)

    
    
def update_instance(mdb, data):
    """
    update instance which match with "input" sha key

    input example;

        r = {
            "datatype": "graph",   # may be polynomial
            "sha": "12b8a0b98077b86f4cff2afbb90c3255c8f9affc",
            "index": "index example",
            "raw": "raw example",
            "features": "features example",
            "semantics": "semantics example",
            "context":  {"edge": {"1": 100, "2": 2000},
                         "vertex": [{"first": 4, "second": 4},
                                    {"first": 3, "second": 55}]},
            "typeset": "typeset example",
            "commit": "update_repo"
        }


    return example;

        {'status': 1}

        if removal is unsuccessful;

        {'status': 0}

    :param data: incoming json file.
    :return:
    """

    datatype = data["datatype"]

    status = 0

    if not os.path.exists(datatype):
        status = 0

    else:
        input_sha = data["sha"]

        dir_index = os.path.join(mdb.get_basedir(), datatype, "index")

        for filename in os.listdir(dir_index):

            if filename == ".git":
                continue

            if input_sha == mdb.get_first_sha(dir_index, filename):
                for attribute in mdb.get_attributes():
                    dir_attribute = os.path.join(mdb.get_basedir(), datatype, attribute)

                    __update_file(mdb, data[attribute], dir_attribute, data["commit"], filename)
                status = 1
                break

    response = {
        "status": status  # if successful otherwise 0
    }

    return response

