import json
import sys
import pprint
import collections
# From https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth

keywords = ["Vertex", "Graph", "Edge", "Directed", "Weighted", "Polyhedron", "Polynomial", "Polytope"]
def get_string_type():
    PY3 = sys.version_info[0] == 3
    if PY3:
        string_types = str
    else:
        string_types = basestring
    return string_types

def isastring(value):
    if isinstance(value, get_string_type()):
        words = get_string(value)
        if not words:
            print("The input is a string but none of them is meaningful. See our keywords:")
            print(keywords)
        else:
            results = get_meaningful_string(words)
            print("The input is a string and they are possible names according to your input")
            print(results)
    else:
        print("The input is not a string. Please enter a string and use at least one in the following keywords:")
        print(keywords)

def get_string(value):
    words = value.split()
    meaningful_words = []
    for word in words:
        if word in keywords:
            meaningful_words.append(word)
    return meaningful_words

def get_meaningful_string(words):
    #ref : https://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python/
    with open("dictionary.index") as dictIndex:
        index = json.load(dictIndex)
    freq_names= {}
    max_value = 1
    for word in words:
        if word in index:
            for name in index[word]:
                if name in freq_names:
                    freq_names[name] = freq_names.get(name) + 1
                    if max_value < freq_names[name]:
                        max_value = freq_names[name]
                else:
                    freq_names[name] = 1
    most_freq_names = []
    for name in freq_names:
        if freq_names[name] == max_value:
            most_freq_names.append(name)
    return most_freq_names

def update_dict(d, u):
    for k, v in u.items():

        if isinstance(d, collections.Mapping):
            if isinstance(v, collections.Mapping):
                r = update_dict(d.get(k, {}), v)
                d[k] = r
            else:
                if k in ["attributes","raw_types"]:
                    tmp = []
                    if k in d:
                        tmp = [ e for e in d[k]]
                    for e in u[k]:
                        if e not in tmp:
                            tmp.append(e)
                    d[k] = tmp
                else:
                    d[k] = u[k]
        else:
            d = {k: u[k]}
    return d

def interpret(name):
    with open("def.index") as defIndex:
        index = json.load(defIndex)
        if name not in index:
            raise Exception("Definition not found in the definition index")
        else:
            # TODO Find correct revision of the file
		    filename = index[name][0]
    with open(filename+".def") as defFile:
        definition = json.load(defFile)
        if "inherits" in definition:
            # TODO resolve dependencies
            parents = definition.pop("inherits")
            for parent in parents:
                parentDef = interpret(parent)
                update_dict(parentDef,definition)
                definition = parentDef
        return definition

def is_of_type(A,B):
    if A == B :
        return True
    with open(A+".def") as Afile:
        A = json.load(Afile)
        if "inherits" in A:
            ret = False
            for parent in A["inherits"]:
                ret = ret | is_of_type(parent,B)
            return ret
    return False


def validate(data):
    with open(data+".data") as dataFile:
        index = json.load(dataFile)
        print(interpret(index["type"]))
    return True



if __name__ == "__main__":
    # execute only if run as a script
    #pprint.pprint(interpret(sys.argv[1]))
    #print("-----------")
    #print(interpret(sys.argv[1]))

    #print(is_of_type(sys.argv[1],sys.argv[2]))
    isastring("Edge Graph")
    #print(isastring("Weighted Graph"))
    #validate("data/polynomial1")
