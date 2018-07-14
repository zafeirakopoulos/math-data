from math_data import math_data


data = math_data()

r = {
    "datatype": "graph",
    "index": "something...",
    "raw": "something...",
    "features": "something...",
    "semantics": "something...",
    "context":  {"edge": {"1": 1, "2": 2},
                 "vertex": [{"first": 2, "second": 1},
                            {"first": 23, "second": 55}]},
    "typeset": "something...",
    "commit": "something..."
}

#firstly add some file after and store its index sha, And you can remove after that
#response = data.add_instance(r)
#print(response)



r = {
    "datatype": "graph",
    "sha": "307fc2e45f95d123cb8a04ae343123ba11e064c9"
}

response = data.remove_instance(r)
print(response)





