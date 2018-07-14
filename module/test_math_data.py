from math_data import math_data


data = math_data()

r = {
    "datatype": "graph",
    "index": "something...",
    "raw": "something...",
    "features": "something...",
    "semantics": "something...",
    "context": "something...",
    "typeset": "something...",
    "commit": "something..."
}

response = data.add_instance(r)

print(response)




