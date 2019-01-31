import json
import sys
import pprint
import collections

def has_property(T,p):
    with open(T+".def") as Tfile:
        T = json.load(Tfile)
        if "properties" in T:
            if p in T["properties"]:
                return T["properties"][p]
            #for P in T["properties"]:
                # TODO path.join
                # TODO get the filename from the def.index
            #    with open("Properties/"+P+".def") as Pfile:
        if "inherits" in T:
            ret = False
            for parent in T["inherits"]:
                ret = ret | has_property(parent,p)
            return ret
    return False


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

if __name__ == "__main__":
	print(is_of_type(sys.argv[1],sys.argv[2]))
    #print(has_property(sys.argv[1],sys.argv[2]))
