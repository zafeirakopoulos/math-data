import json
import sys
import pprint
import collections
from jsonschema import validate

new_path = sys.path[0]
new_path = new_path[:-10] + "/language/"
sys.path[0] = new_path
path_def = new_path[:-23] + "/local/defs/"
print(path_def)
new_path = new_path[:-23] + "/local/third_party/"
print(new_path)
PATH = new_path   #should be changed


def find_def_file(name):
    with open(path_def+"def.index") as defIndex:
        index = json.load(defIndex)

        if name not in index:
            raise Exception("Definition not found in the definition index")
        else:
            # TODO Find correct revision of the file
            filename = index[name][0]
            with open(path_def+filename+".def") as defFile:
                definition = json.load(defFile)
                return definition

def validate(data):
	with open(new_path+data+".json") as dataFile:
		data_file = json.load(dataFile)
		def_file = find_def_file(data_file["name"])
                pprint.pprint(def_file)
	return True

if __name__ == "__main__":
    validate("R100_9gb.col_sparse_Directed Vertex Weighted Graph")

