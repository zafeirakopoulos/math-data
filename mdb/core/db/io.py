from threading import Lock
from mdb.data.db import DB, Table
import os
import json


# This should be a class.
# It is initialized with a local path under which all DB are stored.
# The retrieve functions in this class accept a hask key.
# The key gives url (relative within the MDB, i.e., in the local path given
# when initialized), and a SHA (or a file and SHA depending on the function)
#

class MDB:
    mutex = Lock()
    aspects = ["raw", "features", "semantics", "context", "typeset"]

    def __init__():


    def __add_helper(mdb, data):
        """ Private Helper Function.
        Go through target path and creates new data type
        :param data: incoming json file.
        :return: none
        """


        return result


def add_instance(mdb: DB, data):
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
        sha_list = {}

        for aspect in aspects:

            table = mdb[aspect]

            if isinstance(table, Table):
                result = table.add(data[aspect], data["commit"]) # success: True/False, sha: shakey, error: message

                if result["success"]:
                    sha_list[aspect] = result["sha"]
                else:
                    return result["error"]

        response = mdb["instances"].add(json.dumps(sha_list), "added instance")
        mdb['index'].add("", "add %s" % result['sha'], filename=result['sha'])
    finally:
        mutex.release()

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
    return mdb['index'].remove_file(data['sha'])


def retrieve_instance(mdb, data):

    """ Fetches an instance which match with "input" sha key.
    input example;
        r = {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
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
    filename, stream = mdb["instances"][sha]
    content = json.load(stream)

    instance = {}

    for aspect in aspects:
        _, s = mdb[aspect][content[aspect]]
        instance[aspect] = s.read().decode()

    return instance

def update_instance(mdb, data):
    """
    update instance which match with "input" sha key
    input example;
        r = {
            "sha": "12b8a0b98077b86f4cff2afbb90c3255c8f9affc",
            "raw": "raw example",
            "features": "features example",
            "semantics": "semantics example",
            "context": "graph",
            "typeset": "typeset example",
            "commit": "updated_repo" }
    return example;
        {'status': 1}
        if removal is unsuccessful;
        {'status': 0}
    :param data: incoming json file.
    :return:
    """
    remove_instance(mdb, data)
    return add_instance(mdb, data)


def find(mdb, data):
    """Return the keys of instances matching text.
    """

    datatype = data["datatype"]

    status = ""
    total = 0
    sha = []

    if not os.path.exists(datatype):
        status = datatype + " not found"
    else:

        dir_index = os.path.join(mdb.get_basedir(), datatype, "index")

        # get files in index repo
        for filename in os.listdir(dir_index):

            # ignore .git folder
            if filename == ".git":
                continue

            #
            for attribute in mdb.get_attributes():
                dir_attribute = os.path.join(mdb.get_basedir(), datatype, attribute)

                with open(os.path.join(dir_attribute, filename)) as json_file:
                    text = json.load(json_file)

                if data["text"] in text:
                    status = "True"
                    total += 1
                    sha.append(mdb.get_first_sha(dir_index, filename))
                    break

    response = {
        "sha": json.dumps(sha),  # if successful otherwise 0
        "total": total,
        "status": status
    }

    return response

    # Return SHA keys
    return []

def search(mdb,  text):
    """Return the instances matching text.
    """

def filter(mdb,  criteria):
    """Retrieve instances from the mathdatabase matching criteria.
    """
    instances = []
    return instances
