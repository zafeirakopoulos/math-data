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

    aspect_dic = {}

    if not os.path.exists(mdb.basedir):
        return "Base directory are not found", 0

    # aspects part
    for aspect in mdb.aspects:
        # check if aspect exist

        filename = str(mdb.next_file[aspect]) + ".txt"

        # increase static file number
        mdb.next_file[aspect] += 1

        repo_path = os.path.join(mdb.basedir, aspect, mdb.current_repos[aspect])

        file_path = os.path.join(mdb.basedir, aspect, mdb.current_repos[aspect], filename)

        with open(file_path, 'w') as outfile:
            json.dump(data[aspect], outfile)

        mdb.git_add(repo_path, filename, data["commit"])

        aspect_attributes = {"sha": mdb.get_last_sha(repo_path, filename),
                             "repo": mdb.current_repos[aspect],
                             "file": filename}

        aspect_dic[aspect] = aspect_attributes

        #aspect_dic[aspect] = mdb.get_last_sha(repo_path, filename)

    # Instance part

    instance_file_path = os.path.join(mdb.basedir, "instance", mdb.instance_repo, mdb.instance_file)
    instance_repo_path = os.path.join(mdb.basedir, "instance", mdb.instance_repo)

    # read from instance
    with open(instance_file_path, "r") as json_file:
        sha_list = json.load(json_file)

    # add new dic to instance sha keys
    sha_list.append(aspect_dic)

    # write again updated instance
    with open(os.path.join(instance_file_path), 'w') as outfile:
        json.dump(sha_list, outfile)

        # add and commit instance                          # aspects sha order
    mdb.git_add(instance_repo_path, mdb.instance_file, str(len(sha_list)).zfill(4) + ' - ' + data["commit"])

    # Index part

    index_sha = mdb.get_last_sha(instance_repo_path, mdb.instance_file)

    index_repo_path = os.path.join(mdb.basedir, "index")
    index_file_path = os.path.join(mdb.basedir, "index", mdb.index_file)

    with open(index_file_path, "r") as json_file:
        index_list = json.load(json_file)

    index_list.append({"sha": index_sha,
                       "repo": mdb.instance_repo})

    with open(os.path.join(index_file_path), 'w') as outfile:
        json.dump(index_list, outfile)

    mdb.git_add(index_repo_path, mdb.index_file, data["commit"])

    status = "True"

    return status, index_sha


def add_instance(mdb, data):
    """
    add any instance

    input example;
        r = {
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

    Remove sha key from index file


    input example;

        r = {
            "sha": "a9f870b98077b86f4cff2afbb90c3255c8f9a923"
        }

    return example;

        {'status': True}

        if removal is unsuccessful;

        {'status': False}

    :param data: incoming json file.
    :return: control status
    """

    index_file_path = os.path.join(mdb.basedir, "index", mdb.index_file)

    with open(index_file_path, "r") as json_file:
        sha_list = json.load(json_file)

    if not sha_list:
        return {"status": "There are any instance in index"}

    input_sha = data["sha"]

    for sha in sha_list:

        if input_sha in sha.values():
            sha_list.remove(sha)

            with open(index_file_path, 'w') as outfile:
                json.dump(sha_list, outfile)

            return {"status": True}

    return {"status": False}


def find_instance_order(mdb, sha):

    instance_path = os.path.join(mdb.basedir, "instance")

    for repo in os.listdir(instance_path):

        instance_repo_path = os.path.join(mdb.basedir, "instance", repo)

        for file in os.listdir(instance_repo_path):

            if file == ".git":
                continue

            commits = mdb.get_all_commit(instance_repo_path, file)

            for commit in commits:

                if sha in commit.keys():

                    return file, commit[sha].lstrip('0'), instance_repo_path

    return None, None, "-1"


def retrieve_instance(mdb, data):

    """ Fetches an instance which match with "input" sha key.
    input example;
        r = {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }
        other example
        r = {
            "sha": "21fa767a68101f4b7e75ffe50001954d0ee37a74"
        }

    return example;
        r = {
            "raw": "raw example",
            "features": "features example",
            "semantics": "semantics example",
            "context":  "graph",
            "typeset": "typeset example"
        }
    :param data: incoming json file.
    :return: desired instance
    """

    sha = data["sha"]

    # find instance file  order
    instance_file, order, instance_repo_path = find_instance_order(mdb, sha)

    if instance_repo_path == "-1":
        return {"status": "Instance not found"}

    print(instance_file, order, instance_repo_path)

    # do check out
    mdb.git_checkout(instance_repo_path, sha)

    # read instance file
    with open(os.path.join(instance_repo_path, instance_file), "r") as json_file:
        instance_content = json.load(json_file)

    # do check out
    mdb.git_checkout(instance_repo_path, "master")

    # fetch instance
    aspects = instance_content[int(order) - 1]

    # aspects part

    desired_instance = {}

    for aspect in aspects:

        # aspects repo path
        repo_path = os.path.join(mdb.basedir, aspect, aspects[aspect]["repo"])

        # do check out
        mdb.git_checkout(repo_path, aspects[aspect]["sha"])

        # read aspects file
        with open(os.path.join(repo_path, aspects[aspect]["file"]), "r") as json_file:
            aspect_content = json.load(json_file)

        # do check out
        mdb.git_checkout(repo_path, "master")

        # construct aspects
        desired_instance[aspect] = aspect_content

    return desired_instance


def find_sha_in_index(mdb, sha):

    index_repo_path = os.path.join(mdb.basedir, "index")

    for index_file in os.listdir(index_repo_path):

        if index_file == ".git":
            continue

        with open(os.path.join(index_repo_path, index_file), "r") as json_file:
            sha_repos = json.load(json_file)

            for sha_repo in sha_repos:
                if sha_repo["sha"] == sha:
                    return sha_repo["repo"]

    return "-1"

def update_instance(mdb, data):
    """
    update instance which match with "input" sha key
    input example;
        r = {
            "sha": "12b8a0b98077b86f4cff2afbb90c3255c8f9affc",
            "index": "index example",
            "raw": "raw example",
            "features": "features example",
            "semantics": "semantics example",
            "context":  {"edge": {"1": 100, "2": 2000},
                         "vertex": [{"first": 4, "second": 4},
                                    {"first": 3, "second": 55}]},
            "typeset": "typeset example",
            "commit": "updated_repo" }
    return example;
        {'status': 1}
        if removal is unsuccessful;
        {'status': 0}
    :param data: incoming json file.
    :return:
    """

    input_sha = data["sha"]

    repo = find_sha_in_index(mdb, input_sha)

    if repo == "-1":
        return {"status": "Instance not found"}




    print(repo)




    return None

