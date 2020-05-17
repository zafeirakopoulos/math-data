import os
import json
from mdb.backend.db.db import MathDataBase

def init_mdb(mdb_path,mdb_name,mdb_definition):
    mdb = MathDataBase(mdb_path,mdb_name,mdb_definition)

    if not mdb.already_exists:
    #   Import a sample dataset to exhibit the functionality.
    #   One datastructure, instance, dataset and formatter
        datastructure = '{ "name": "Test Datastructure", "raw": {"features": 55}} '
        mdb.add_datastructure(datastructure,"Example Datastructure")
        pending=mdb.pending_datastructures()
        mdb.approve_datastructure(pending[0],"It's a good example")
    return mdb
