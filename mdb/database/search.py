import os
from git import Repo
import json


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
