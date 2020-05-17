import os
import json
from mdb.backend.db.db import MathDataBase

def init_mdb(mdb_path,mdb_name,mdb_definition):
    mdb = MathDataBase(mdb_path,mdb_name,mdb_definition)

    if not mdb.already_exists:
    #   Initialize the mdb with data from local
        #print(os.listdir(os.path.join(mdb_path,"local", "definitions")))
        for ds_filename in os.listdir(os.path.join(mdb_path,"local", "datastructures")):
            with open(os.path.join(mdb_path,"local", "datastructures",ds_filename)) as def_file:
                datastructure = def_file.read()
                mdb.add_datastructure(datastructure,"Example Datastructure")
                pending=mdb.pending_datastructures()
                mdb.approve_datastructure(pending[0],"Imported from local/datastructures")

        #datastructure = '{ "name": "Test Datastructure", "raw": {"features": 55}} '
        #mdb.add_datastructure(datastructure,"Example Datastructure")
        #pending=mdb.pending_datastructures()
        #mdb.approve_datastructure(pending[0],"It's a good example")
    return mdb
