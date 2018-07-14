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

response = data.add_instance(r)
print(response)






