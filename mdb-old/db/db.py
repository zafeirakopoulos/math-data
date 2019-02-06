import json
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os


class MathDataBase:
    """A MathData database."""
    base_path = None
    name = None
    definition = None

    def __init__(self,path,name,definition=None):
        """Initializes a MathDataBase given a definition, a path and a name.
        If no definition is given, it will return an existing MathDataDase.

        :param path: Path of the new MathDataDase in the filesystem
        :param name: Name of the MathDataBase (it will be the folder name)
        :param definition: A valid MathDataBase definiton as json string
        :returns: A MathDataBase instance"""

        self.name = name
        # The base path is the path and the name
        self.base_path = os.path.join(path, self.name)+".git"

        if definition!=None:
            self.definition = json.loads(definition)
            # Create a bare repository in base_path
            #subprocess.call(["git", "init", "--bare", self.base_path])
            subprocess.call(["git", "init", self.base_path])

        # Change to the directory of the repository,
        # so that following commands will be executed in the repo
        os.chdir(self.base_path)

        if definition!=None:
            # Write the definition so that it can be read later
            with open('mdb_def.txt', 'w') as mdb_definition:
                mdb_definition.write(json.dumps(self.definition)+'\n')
        else:
            with open('mdb_def.txt', 'r') as mdb_definition:
                self.definition = mdb_definition.read()

    ########################################################################
    ########################################################################
    ##########################  Add  #######################################
    ########################################################################
    ########################################################################

    def add_data_to_repo(self, data, path=None):
        """Add data to the repository.

        :param data: The data to be stored
        :param path: Path of the new MathDataDase in the filesystem
        :returns: The SHA key of the object

        .. warnings also:: Not exposed to API."""
        os.chdir(self.base_path)
        process = Popen(["git", "hash-object", "-w", "--stdin", "--path", path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(data))[0]
        return stdo.decode()[:-1]


    def add_instance_to_database(self, data):
        os.chdir(self.base_path)
        for path in self.definition["paths"]:
            if path in data:
                data_key = self.add_data_to_repo(path, str(data[path]))
                subprocess.check_output(["git", "update-index", "--add", "--cacheinfo", "100644",data_key, path]).decode()
        return subprocess.check_output(["git", "write-tree"]).decode()[:-1]


    def add_dataset(self, dataset):
        """Register a dataset in the MathDataBase.

        :param definition: A JSON object defining a dataset
        :returns: The SHA key of the dataset"""
        os.chdir(self.base_path)
        # It stores datasets under the "datasets" path
        process = Popen(["git", "hash-object", "-w", "--stdin", "--path", "datasets"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(data))[0]
        dataset_key = stdo.decode()[:-1]
        subprocess.check_output(["git", "update-index", "--add", "--cacheinfo", "100644",dataset_key, "datasets"]).decode()
        return subprocess.check_output(["git", "write-tree"]).decode()[:-1]


    def add_definition(self, definition):
        """Register a definition in the MathDataBase.

        :param definition: A JSON object as a string
        :returns: The SHA key of the definition"""
        os.chdir(self.base_path)
        # It stores definitions under the "definitions" path
        process = Popen(["git", "hash-object", "-w", "--stdin", "--path", "definitions"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(definition))[0]
        def_key = stdo.decode()[:-1]
        subprocess.check_output(["git", "update-index", "--add", "--cacheinfo", "100644",def_key, "definitions"]).decode()
        return subprocess.check_output(["git", "write-tree"]).decode()[:-1]

    ########################################################################
    ########################################################################
    ##########################  Retrieve  ##################################
    ########################################################################
    ########################################################################

    def retrieve_instance_from_repo(self,repo,key):
        os.chdir(self.base_path)
        return subprocess.check_output(["git", "cat-file", "-p", key]).decode()

    def retrieve_instance_from_database(self, key):
        response = []
        for path in self.definition["paths"]:
            try:
                response.append( '"'+path+'":'+subprocess.check_output(["git", "show", key+":"+path]).decode())
            except:
                pass
        return ",".join(response)


    def retrieve_definition(self, key):
        """Get the definition registered under the given key.

        :param key: The SHA key of the definition
        :returns: A JSON object as a string"""
        # return subprocess.check_output(["git", "diff", key]).decode()
        response = subprocess.check_output(["git", "diff", key]).decode().split("\n")[1:]
        return response


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

    def approve_definition(self,key, message):
        os.chdir(self.base_path)
        response = subprocess.check_output(["git", "commit-tree", key, "-m", message]).decode()[:-1]
        with open('definition_index.txt', 'a') as mdb_index:
            mdb_index.write(response+'\n')
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
            return [ line for line in mdb_index]
