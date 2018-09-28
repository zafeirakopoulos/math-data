import json
import sys
import pprint
import collections

# From https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
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

def validate(name,data):

    return True

if __name__ == "__main__":
    # execute only if run as a script
    #pprint.pprint(interpret(sys.argv[1]))
    #print("-----------")
    #print(interpret(sys.argv[1]))
    print(is_of_type(sys.argv[1],sys.argv[2]))
