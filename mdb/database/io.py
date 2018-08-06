from threading import Lock
from mdb.util.db import DB, Table
import os
import json


mutex = Lock()

aspects = ["raw", "features", "semantics", "context", "typeset"]

def __add_helper(mdb, data):
    """ Private Helper Function.
    Go through target path and creates new data type
    :param data: incoming json file.
    :return: none
    """

    sha_list = {}

    for aspect in aspects:

        table = mdb[aspect]

        if isinstance(table, Table):
            result = table.add(data[aspect], data["commit"]) # success: True/False, sha: shakey, error: message

            if result["success"]:
                sha_list[aspect] = result["sha"]
            else:
                return result["error"]

    result = mdb["instances"].add(json.dumps(sha_list), "added instance")
    mdb['index'].add("", "add %s" % result['sha'], filename=result['sha'])

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
        response = __add_helper(mdb, data)
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
        instance[aspect] = s.read()

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

