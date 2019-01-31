import os
import json
from mdb.db.db import MathDataBase

def init_mdb(mdb_path,mdb_name,mdb_definition):
    mdb = MathDataBase(mdb_path,mdb_name,mdb_definition)

    data = '{"name": "Directed Edge and Vertex Weighted Graph", "raw": {"dense": {"edges": [[10, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 10, 0, 9, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 7, 0, 0], [0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 10, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 10, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 9, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 2, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]], "vertices": [5, 1, 5, 7, 9, 8, 7, 6, 9, 6, 8, 4, 3, 10, 4, 5, 2, 2, 10, 7]}}, "raw_types": {"dense": true, "sparse": false}, "attributes": {"edges": true, "vertices": true}, "plural": "Directed Edge and Vertex Weighted Graphs", "options": {"edges": {"directed": true, "weighted": true}, "vertices": {"weighted": true}}, "size": {"edges": 40, "vertices": 20}}'

    data2 = '{"name": "Directed Edge and Vertex Weighted Graph", "raw": {"dewdew":55}, "options": {"dewetrue":3}, "size": {"edges": 40, "vertices": 20}}'

    data_json = json.loads(data)
    tree = mdb.add_instance_to_database(data_json)
    print(mdb.retrieve_instance_from_database(tree))
    ckey = mdb.approve_instance(tree, "First one ever")
    print(ckey)

    data_json = json.loads(data2)
    tree = mdb.add_instance_to_database(data_json)
    print(mdb.retrieve_instance_from_database(tree))
    ckey = mdb.approve_instance(tree, "Second one ever")
    print(ckey)

    return mdb
