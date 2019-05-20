import json
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os
from mdb.md_def import *


class MathDataBase:
    """A MathData database."""
    base_path = None
    name = None
    definition = None

    def __init__(self,path,name, mdb_def=None):
        """Initializes a MathDataBase given a definition, a path and a name.
        If no definition is given, it will return an existing MathDataDase.

        :param path: Path of the new MathDataDase in the filesystem
        :param name: Name of the MathDataBase (it will be the folder name)
        :param definition: A valid MathDataBase definiton as json string
        :returns: A MathDataBase instance"""

        self.name = name
        # The base path is the path and the name
        self.base_path = os.path.join(path, self.name)+".git"
        if mdb_def!=None:
            self.definition = json.loads(mdb_def)
            # Create a bare repository in base_path
            #subprocess.call(["git", "init", "--bare", self.base_path])
            subprocess.call(["git", "init", self.base_path])

        # Change to the directory of the repository,
        # so that following commands will be executed in the repo
        os.chdir(self.base_path)

        if mdb_def!=None:
            # Write the definition so that it can be read later
            with open('mdb_def.txt', 'w') as mdb_definition:
                mdb_definition.write(json.dumps(self.definition)+'\n')
        else:
            with open('mdb_def.txt', 'r') as mdb_definition:
                self.definition = mdb_definition.read()

        for entity in self.definition["entities"]:

            # Create entity_index file
            with open(entity+'_index.txt', 'w') as tmp:
                pass

            # Create entity_pending file
            with open(entity+'_pending.txt', 'w') as tmp:
                pass

            os.mkdir(entity)
            with open(os.path.join(entity,'.gitkeep'), 'w') as tmp:
                pass

        # Commit the initial state of MDB. This enables also the creation of branches.
        subprocess.call(["git", "add", "*"])
        subprocess.call(["git", "commit", "-m", "Initialization of MDB"])

        # Create the default branch, so that we do not commit in master
        subprocess.call(["git", "branch", self.definition["default_branch"]])
        subprocess.call(["git", "checkout", self.definition["default_branch"]])

    ########################################################################
    ########################################################################
    ##########################  Datastructure ##############################
    ########################################################################
    ########################################################################


    def add_datastructure(self, datastructure, message):
        """Register a datastructure in the MathDataBase.
        It is added in the pending list waiting for approval by an editor.

        :param datastructure: A JSON object as a string
        :param message: A description of the datastructure (the commit message)
        :returns: The name of the branch in which the datastructure was commited"""
        # It stores datastructures under the "datastructure" path
        os.chdir(os.path.join(mdb_root,self.base_path,"datastructure"))

        # Get the hash of the file
        process = Popen(["git", "hash-object", "--stdin", "--path", "datastructure"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(datastructure))[0]
        hash = stdo.decode()[:-1]

        # Create a new branch in the repo with name the hash of the datastructure
        subprocess.check_output(["git", "branch", hash]).decode()[:-1]
        # TODO: Check if fail
        subprocess.check_output(["git", "checkout", hash]).decode()[:-1]
        # TODO: Check if fail

        # Write the file
        with open(hash, 'w') as datastructure_file:
            datastructure_file.write(datastructure)

        # Add and commit in the new branch
        subprocess.check_output(["git", "add", os.path.join(mdb_root,self.base_path,"datastructure",hash) ]).decode()[:-1]
        subprocess.check_output(["git", "commit", "-m", message]).decode()[:-1]
        commit_hash = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:'%H'"]).decode()[:-1]


        # Add the branch name in the pending list at the default_branch.
        subprocess.check_output(["git", "checkout", self.definition["default_branch"]]).decode()[:-1]
        # TODO: Check if fail
        with open(os.path.join(mdb_root,self.base_path,'datastructure_pending.txt'), 'a') as datastructure_pending:
            datastructure_pending.write(commit_hash+"\n")

        # Return 0 on success
        return 0


    def approve_datastructure(self, commit_hash, message):
        os.chdir(os.path.join(mdb_root,self.base_path))

        # Remove from pending list
        with open("datastructure_pending.txt", "r") as datastructure_pending:
            lines = datastructure_pending.readlines()
        with open("datastructure_pending.txt", "w") as datastructure_pending:
            for line in lines:
                if line.strip("'").strip("\n") != commit_hash:
                    datastructure_pending.write(line.strip("'").strip("\n")+"\n")

        # TODO: Not thread safe! Assumes we are in default_branch.
        subprocess.check_output(["git", "merge", "-m", message, commit_hash]).decode()[:-1]

        # Add merge in index list
        with open('datastructure_index.txt', 'a') as datastructure_index:
                datastructure_index.write(commit_hash+"\n")
        # Commit the new index in the default_branch
        subprocess.check_output(["git", "add", os.path.join(mdb_root,self.base_path,'datastructure_index.txt') ]).decode()[:-1]
        subprocess.check_output(["git", "commit", "-m", "Merged datastructure "+commit_hash]).decode()[:-1]

        return 0

    def pending_datastructures(self):
        os.chdir(os.path.join(mdb_root,self.base_path))

        with open("datastructure_pending.txt", "r") as datastructure_pending:
            lines = datastructure_pending.readlines()
        return [ line.strip("'").strip("\n") for line in lines ]

    def get_datastructures(self):
        os.chdir(os.path.join(mdb_root,self.base_path))

        with open("datastructure_index.txt", "r") as datastructure_index:
            lines = datastructure_index.readlines()
        return [ line.strip("\n") for line in lines ]

    def retrieve_datastructure(self, hash):
        files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hash ]).decode()[:-1]
        files = files.split("\n")
        if len(files)>1:
            raise Exception("More than one files in the commit")
        with open(os.path.join(mdb_root,self.base_path, files[0])) as datastructure:
            lines = datastructure.readlines()
        # TODO: \n or other newline feed?
        return "\n".join(lines)

    ########################################################################
    ########################################################################
    ##########################  Formatter  #################################
    ########################################################################
    ########################################################################


    def add_object(self, data, name):
        # Go to the pending directory of the entity
        os.chdir(os.path.join(name,"pending"))

        # Get the hash of the data, to be used as filename
        process = Popen(["git", "hash-object", "--stdin", "--path", name], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(data))[0]
        object_hash = stdo.decode()[:-1]

        # Write the data to a file
        with open(object_hash, 'w') as object_file:
            object_file.write(data)

        # Add the key to the pending list
        os.chdir(os.path.join(mdb_root,self.base_path))
        print(os.path.join(mdb_root,self.base_path))
        with open(name+"_pending.txt", 'a') as object_index:
            object_index.write(object_hash+'\n')
        return 0

    def approve_object(self, object_hash, name):
        #TODO: better message
        message = "commited data" + object_hash

        # Go to the root of the repository
        os.chdir(os.path.join(mdb_root,self.base_path))

        # Remove key from the pending list
        with open(name+"_pending.txt", "r") as object_index:
            lines = object_index.readlines()
        with open(name+"_pending.txt", "w") as object_index:
            for line in lines:
                if line.strip("\n") != object_hash:
                    object_index.write(line)

        # TODO: check if file exists already
        subprocess.check_output(["mv", os.path.join(mdb_root,self.base_path,name,"pending",object_hash), os.path.join(mdb_root,self.base_path,"instance",object_hash) ])
        subprocess.check_output(["git", "add",  os.path.join(mdb_root,self.base_path,name,object_hash)]).decode()[:-1]

        # Commit
        commit_key = subprocess.check_output(["git", "commit", "-m", message]).decode()[:-1]

        # Add the key to the index list
        with open(name+"_index.txt", 'a') as object_index:
            object_index.write(commit_key+'\n')



    def retrieve_pending(self):
        # It will simulate the commit and return the results to the editor's UI
        return 0

    def add_instance(self, data, def_version):
        """Register an istance in the MathDataBase.
        It is added in the pending list waiting for approval by an editor.

        :param data: A JSON object defining the instance
        :returns: The SHA key of the instance"""
        os.chdir(self.base_path)

        # add data to repo as json_dump not string so that we can get it correctly
        for path in self.definition["paths"]:
            if path in data:
                data_key = self.add_data_to_repo(json.dumps(data[path]),path)
                # TODO: Why decode?
                subprocess.check_output(["git", "update-index", "--add", "--cacheinfo", "100644",data_key, path]).decode()
        data_key = self.add_data_to_repo(def_version,"definition_version")
        # TODO: Why decode?
        subprocess.check_output(["git", "update-index", "--add", "--cacheinfo", "100644",data_key, "definition_version"]).decode()
        # After updating the different paths, we write the tree and return the hash key.
        return subprocess.check_output(["git", "write-tree"]).decode()[:-1]


    def add_dataset(self, dataset):
        """Register a dataset in the MathDataBase.
        It is added in the pending list waiting for approval by an editor.

        :param definition: A JSON object defining a dataset
        :returns: The SHA key of the dataset"""
        os.chdir(self.base_path)
        # It stores datasets under the "datasets" path
        process = Popen(["git", "hash-object", "-w", "--stdin", "--path", "datasets"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(data))[0]
        dataset_key = stdo.decode()[:-1]
        subprocess.check_output(["git", "update-index", "--add", "--cacheinfo", "100644",dataset_key, "datasets"]).decode()
        return subprocess.check_output(["git", "write-tree"]).decode()[:-1]


    def add_formatter(self, formatter):
        """Register a formatter in the MathDataBase.

        :param formatter: A JSON object as a string
        :returns: The SHA key of the formatter"""
        os.chdir(self.base_path)
        # It stores formatter definitions under the "formatters" path
        process = Popen(["git", "hash-object", "-w", "--stdin", "--path", "formatters"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(json.dumps(formatter)))[0]
        formatter_key = stdo.decode()[:-1]
        subprocess.check_output(["git", "update-index", "--add", "--cacheinfo", "100644",formatter_key, "formatters"]).decode()
        return subprocess.check_output(["git", "write-tree"]).decode()[:-1]

    ########################################################################
    ########################################################################
    ##########################  Retrieve  ##################################
    ########################################################################
    ########################################################################

    def retrieve_instance_from_database(self, key):
        # initialize output as object
        response = {}
        for path in self.definition["paths"]:
            try:
                # get data as json (because we added the data as json)
                response[path] = json.loads(subprocess.check_output(["git", "show", key+":"+path]).decode())
            except:
                pass

        # add definition_version to output
        response["definition_version"] = subprocess.check_output(["git", "show", key+":definition_version"]).decode()

        # return output as json dump so that we can use it correctly
        return json.dumps(response)


    def retrieve_definition(self, key):
        """Get the definition registered under the given key.

        :param key: The SHA key of the definition
        :returns: A JSON object as a string"""
        return subprocess.check_output(["git", "show", key+":"+"definitions"]).decode()
        #response = subprocess.check_output(["git", "diff", key]).decode().split("\n")[1:]
        #return response

    def retrieve_formatter_signature(self, key):
        """Get the formatter signature registered under the given key.

        :param key: The SHA key of the formatter
        :returns: A JSON object as a string"""
        data = JSON.loads(subprocess.check_output(["git", "show", key+":"+"formatters"]).decode())
        return data["to"]

    ########################################################################
    ########################################################################
    ##########################  Approve   ##################################
    ########################################################################
    ########################################################################
    def approve_instance(self,key, message):
        os.chdir(self.base_path)
        response = subprocess.check_output(["git", "commit-tree", key, "-m", message]).decode()[:-1]
        with open('instance_index.txt', 'a') as mdb_index:
            mdb_index.write(response+'\n')
        return response



    def approve_formatter(self,formatter,key, message):
        os.chdir(self.base_path)
        response = subprocess.check_output(["git", "commit-tree", key, "-m", message]).decode()[:-1]
        formatter_index = {}
        with open('formatter_index.txt', 'r') as mdb_index:
            try:
                formatter_index = json.load(mdb_index)
            except:
                pass
        with open('formatter_index.txt', 'w') as mdb_index:
            from_version_key = formatter["from"]["version"]
            if from_version_key in formatter_index.keys():
                formatter_index[from_version_key].append(key)
            else:
                formatter_index[from_version_key] = [key]
            mdb_index.write(json.dumps(formatter_index))
        return response
    ########################################################################
    ########################################################################
    ##########################  Indices ####################################
    ########################################################################
    ########################################################################

    def dataset_index(self):
        """Get all the datasets currently registered in the MathDataDase.

        :returns: List of keys for the registered datasets"""
        os.chdir(self.base_path)
        with open('dataset_index.txt', 'r') as mdb_index:
            return [ line for line in mdb_index]

    def instance_index(self):
        """Get all the instances currently registered in the MathDataDase.

        :returns: List of keys for the registered instances"""
        os.chdir(self.base_path)
        with open('instance_index.txt', 'r') as mdb_index:
            return [ line for line in mdb_index]

    def definition_index(self):
        """Get all the definitions currently registered in the MathDataDase.

        :returns: List of keys for the registered definitions"""
        os.chdir(self.base_path)
        with open('definition_index.txt', 'r') as mdb_index:
            return json.load(mdb_index)

    def formatter_index(self):
        """Get all the formatters currently registered in the MathDataDase.

        :returns: List of keys for the registered formatters"""
        os.chdir(self.base_path)
        with open('formatter_index.txt', 'r') as mdb_index:
            return json.load(mdb_index)
