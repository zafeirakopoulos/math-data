import os
import json
from mdb.backend.db.db import MathDataBase

def init_mdb(mdb_path,mdb_name,mdb_definition):
    mdb = MathDataBase(mdb_path,mdb_name,mdb_definition)

    data = '{ "name": "Directed Edge and Vertex Weighted Graph", "raw": {"dense": {"edges": [' +\
        '[10, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' +\
        '[0, 10, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' +\
        '[0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' +\
        '[0, 0, 0, 10, 0, 9, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 7, 0, 0], ' +\
        '[0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 10, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 6, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 5, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 10, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 9, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 2, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 2, 7], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5], ' +\
        '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]], "vertices": [5, 1, 5, 7, 9, 8, 7, 6, 9, 6, 8, 4, 3, 10, 4, 5, 2, 2, 10, 7]}}, "raw_types": {"dense": true, "sparse": false}, "attributes": {"edges": true, "vertices": true}, "plural": "Directed Edge and Vertex Weighted Graphs", "options": {"edges": {"directed": true, "weighted": true}, "vertices": {"weighted": true} }, "size": {"edges": 40, "vertices": 20}}'

    datastructure1 = '{ "name": "Directed Edge and Vertex Weighted Graph", "raw": {"dewdew": 55}, "options": {"dewetrue": 3}, "size": {"edges": 40, "vertices": 20} }'
    datastructure2 = '{ "name": "Directed Graph", "raw": {"dewdew": 11}, "options": {"dd": 3}}'

    # def_version="22ac84f9b99e024dad8e98bc1d2c7c4b03cdd71e"
    # data_json = json.loads(data)
    # tree = mdb.add_instance_to_database(data_json,def_version)
    #print(mdb.retrieve_instance_from_database(tree))
    # ckey = mdb.approve_instance(tree, "First one ever")
    #print(ckey)

    # data_json = json.loads(data2)
    # tree = mdb.add_instance_to_database(data_json,def_version)
    #print(mdb.retrieve_instance_from_database(tree))
    # ckey = mdb.approve_instance(tree, "Second one ever")
    #print(ckey)

    # formate = '{"from": { "type":"graph", "format":"MathDataJSON", "version": "ab5d9ad418600aa01e35d414207ef1acfcd64c84"  }, "to": {"type":"graph", "format":"dimacs", "version": ""},"template":"thetemplate"}'
    # data_formatter = json.loads(formate)
    # tree = mdb.add_formatter(data_formatter)
    # ckey = mdb.approve_formatter(data_formatter,tree, "fromatter")
    # #print(ckey)
    # formate = '{"from": { "type":"graph", "format":"MathDataJSON", "version": ""  }, "to": {"type":"graph", "format":"gizem", "version": ""},"template":"thetemplate"}'
    # data_formatter = json.loads(formate)
    # tree = mdb.add_formatter(data_formatter)
    # ckey = mdb.approve_formatter(data_formatter,tree, "fromatter")

    #mdb.add_object(data,"instance")
    #mdb.approve_object("5d0d1b9129e495f94999e2678c95418ce2a04d7b", "instance")

    if not mdb.already_exists:
        mdb.add_datastructure(datastructure1,"Directed weighted graphs")
        mdb.add_datastructure(datastructure2,"Directed graphs")

        print("-------")
        pending=mdb.pending_datastructures()
        print(pending)
        mdb.approve_datastructure(pending[0],"It's good")
        print("-------")
        pending=mdb.pending_datastructures()
        print(pending)
        mdb.approve_datastructure(pending[0],"It's good")
        pending=mdb.pending_datastructures()
        print(pending)

        print("========")
        datastructures = mdb.get_datastructures()
        print(datastructures)
        print("==*****===****===")
        ds = mdb.retrieve_datastructure(datastructures[0])
        print(ds)

        mdb.add_instance(data, "Adding first instance")
        print("-------")
        pending=mdb.pending_instances()
        print(pending)
        mdb.approve_instance(pending[0], "It's good")
        print("-------")
        pending=mdb.pending_datastructures()
        print(pending)

        print("========")
        instances = mdb.get_instances()
        print(instances)
        print("==*****===****===")
        instance = mdb.retrieve_instance(instances[0])
        print(instance)


    return mdb
