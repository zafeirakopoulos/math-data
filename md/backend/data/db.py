import json
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os
from md.md_def import *
from md.backend.repository_database.index_database import IndexDatabase 
import tarfile

class MathDataBase:
    """A MathData database."""
    base_path = None # path for git database
    repo_paths = [] # list of paths of created repositories when first one bloats
    name = None
    definition = None
    already_exists = False
    MAX_REPOSITORY_SIZE_MB = 3 # if repo size > this amount in MB, we will create new repository

    def __init__(self,path,name, mdb_def=None):
        """Initializes a MathDataBase given a definition, a path and a name.
        If no definition is given, it will return an existing MathDataDase.

        :param path: Path of the new MathDataDase in the filesystem
        :param name: Name of the MathDataBase (it will be the folder name)
        :param definition: A valid MathDataBase definiton as json string
        :returns: A MathDataBase instance"""

        self.name = name
        self.path = path
        self.mdb_def = mdb_def # will use while creating new repositories
        # The base path is the path and the name
        self.base_path = os.path.join(path, self.name)+".git"
        if os.path.exists(self.base_path):
            self.index_db = IndexDatabase(self.path,self.name)
        else:
            self.index_db = IndexDatabase(self.path, self.name, True)
        self.init_and_set_directory(self.base_path, mdb_def)

    def init_and_set_directory(self, base_path, mdb_def=None):
        self.base_path = base_path
        if os.path.exists(self.base_path):
            os.chdir(self.base_path)
            with open('mdb_def.txt', 'r') as mdb_definition:
                self.definition = json.loads(mdb_definition.read())

            subprocess.call(["git", "checkout", self.definition["default_branch"]])
            self.already_exists = True

        else:
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

                #os.mkdir(entity)
                try:
                    os.mkdir(entity)
                except:
                    pass

                with open(os.path.join(entity,'.gitkeep'), 'w') as tmp:
                    pass

            try:
                os.mkdir("scratch")
            except:
                pass
            with open(os.path.join("scratch",'.gitkeep'), 'w') as tmp:
                pass

            try:
                os.mkdir("import_scratch")
            except:
                pass
            with open(os.path.join("import_scratch",'.gitkeep'), 'w') as tmp:
                pass



            # Commit the initial state of MDB. This enables also the creation of branches.
            subprocess.call(["git", "add", "*"])
            subprocess.call(["git", "commit", "-m", "Initialization of MDB"])

            # Create the default branch, so that we do not commit in master
            subprocess.call(["git", "branch", self.definition["default_branch"]])
            subprocess.call(["git", "checkout", self.definition["default_branch"]])


########################################################################
########################################################################
##########################  Helpers  ###################################
########################################################################
########################################################################

    def remove_hash_from_pending(self, commit_hash, pending_file_name):
        # Remove from pending list
        self.cd_to_commit_repository(commit_hash)
        with open(pending_file_name, "r") as pending_file:
            lines = pending_file.readlines()
        with open(pending_file_name, "w") as pending_file:
            for line in lines:
                if line.strip("'").strip("\n") != commit_hash:
                    pending_file.write(line.strip("'").strip("\n")+"\n")


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
        (self.base_path, available_repo_id) = self.get_available_repository()
        os.chdir(os.path.join(self.base_path, "datastructure"))

        # Get the hash of the file
        process = Popen(["git", "hash-object", "--stdin", "--path", "datastructure"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(datastructure))[0]
        hash = stdo.decode()[:-1]

        # Create a new branch in the repo with name the hash of the datastructure
        subprocess.call(["git", "branch", hash])
        # TODO: Check if fail
        subprocess.call(["git", "checkout", hash])
        # TODO: Check if fail

        # Write the file
        with open(hash, 'w') as datastructure_file:
            datastructure_file.write(datastructure)

        # Add and commit in the new branch
        subprocess.call(["git", "add", os.path.join(self.base_path, "datastructure", hash) ])
        subprocess.call(["git", "commit", "-m", message])

        commit_hash = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:'%H'"]).decode()[:-1]


        # Add the branch name in the pending list at the default_branch.
        subprocess.call(["git", "checkout", self.definition["default_branch"]])

        # TODO: Check if fail
        with open(os.path.join(self.base_path, 'datastructure_pending.txt'), 'a') as datastructure_pending:
            datastructure_pending.write(commit_hash+"\n")

        self.index_db.sql_add_commit(commit_hash, available_repo_id)
        return "ok"


    def approve_datastructure(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        index_file_name = 'datastructure_index.txt'

        self.remove_hash_from_pending(commit_hash, "datastructure_pending.txt")

        # TODO: Not thread safe! Assumes we are in default_branch.
        subprocess.check_output(["git", "merge", "-m", message, commit_hash])

        # Add merge in index list
        with open(index_file_name, 'a') as datastructure_index:
                datastructure_index.write(commit_hash+"\n")

        # Commit the new index in the default_branch
        subprocess.check_output(["git", "add", os.path.join(self.base_path, index_file_name) ])
        subprocess.check_output(["git", "commit", "-m", "Merged datastructure "+commit_hash])

        return 0

    def reject_datastructure(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        self.remove_hash_from_pending(commit_hash,"datastructure_pending.txt")


    def get_diff(self, commit_hash):
        self.cd_to_commit_repository(commit_hash)
        diff = subprocess.check_output(["git", "show", commit_hash]).decode()[:-1]
        return diff


    def pending_datastructures(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )

        with open("datastructure_pending.txt", "r") as datastructure_pending:
            lines = datastructure_pending.readlines()

        result = [ line.strip("'").strip("\n") for line in lines ]
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.pending_datastructures(step+1, repo_count)
        return result

    def get_datastructures(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )

        with open("datastructure_index.txt", "r") as datastructure_index:
            lines = datastructure_index.readlines()
        result = [ line.strip("\n") for line in lines ]

        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.get_datastructures(step+1, repo_count)
        return result

    def retrieve_datastructure(self, hash):
        self.cd_to_commit_repository(hash)
        files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hash ]).decode()[:-1]
        files = files.split("\n")

        if len(files) == 0:
            return "0 files!"

        if len(files)>1:
            return "More than one files in the commit"

        with open(os.path.join(self.base_path, files[0])) as datastructure:
            lines = datastructure.readlines()
        # TODO: \n or other newline feed?
        return "\n".join(lines)


    ########################################################################
    ########################################################################
    ##########################  Instance   #################################
    ########################################################################
    ########################################################################


    def add_instance(self, instance, message):
        """Register an instance in the MathDataBase.
        It is added in the pending list waiting for approval by an editor.

        :param instance: A JSON object as a string
        :param message: A description of the instance (the commit message)
        :returns: The name of the branch in which the instance was commited"""
        print("In add instance")

        # Split the raw data in the instance to be stored
        # Raw data are stored as git object to remove redundancy
        # It stores raw data under the "instance" path
        (self.base_path, available_repo_id) = self.get_available_repository()
        os.chdir(os.path.join(self.base_path, "instance"))
        process = Popen(["git", "hash-object", "-w", "--stdin", "--path", "instance"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(instance))[0]
        hash = stdo.decode()[:-1]

         # Create a new branch in the repo with name the hash of the instance
        subprocess.check_output(["git", "branch", hash]).decode()[:-1]


        # TODO: Check if fail
        subprocess.check_output(["git", "checkout", hash]).decode()[:-1]
        # TODO: Check if fail

        # Write the file
        with open(hash, 'w') as instance_file:
            instance_file.write(instance)


        # Add and commit in the new branch
        subprocess.call(["git", "add", os.path.join(self.base_path, "instance", hash) ])

        subprocess.call(["git", "commit", "-m", message])

        commit_hash = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:'%H'"]).decode()[:-1]


        # Add the branch name in the pending list at the default_branch.
        subprocess.check_output(["git", "checkout", self.definition["default_branch"]])
        # TODO: Check if fail
        with open(os.path.join(self.base_path,'instance_pending.txt'), 'a') as instance_pending:
            instance_pending.write(commit_hash+"\n")

        self.index_db.sql_add_commit(commit_hash, available_repo_id)
        return commit_hash + " added."

    def approve_instance(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        index_file_name = 'instance_index.txt'

        self.remove_hash_from_pending(commit_hash, "instance_pending.txt")

        # TODO: Not thread safe! Assumes we are in default_branch.
        subprocess.check_output(["git", "merge", "-m", message, commit_hash])

        # Add merge in index list
        with open(index_file_name, 'a') as index_file:
                index_file.write(commit_hash+"\n")

        # Commit the new index in the default_branch
        subprocess.check_output(["git", "add", os.path.join(self.base_path, index_file_name) ])
        subprocess.check_output(["git", "commit", "-m", "Merged datastructure "+commit_hash])

        return 0

    def reject_instance(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        self.remove_hash_from_pending(commit_hash,"instance_pending.txt")

    def pending_instances(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir(self.base_path)

        with open("instance_pending.txt", "r") as pending_file:
            lines = pending_file.readlines()
        result = [ line.strip("'").strip("\n") for line in lines ]
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.pending_instances(step+1, repo_count)
        return result

    def get_instances(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )

        with open("instance_index.txt", "r") as index_file:
            lines = index_file.readlines()

        result = [ line.strip("\n") for line in lines ]
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.get_instances(step+1, repo_count)
        return result


    def get_instances_by_datastructure(self,datastructure, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )
        response = []
        with open("instance_index.txt", "r") as index_file:
            keys = [str(line.strip("\n")) for line in index_file.readlines()]
            for key in keys:
                # To slow? Dont convert to json
                if json.loads(self.retrieve_instance(key))["datastructure"] == datastructure:
                    response.append(key)
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            response += self.get_instances_by_datastructure(datastructure, step+1, repo_count)
        return response



    def retrieve_instance(self, hash):
        self.cd_to_commit_repository(hash)
        files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hash ]).decode()[:-1]
        files = files.split("\n")

        if len(files) == 0:
            return "0 files!"

        if len(files)>1:
            return "More than one files in the commit"

        with open(os.path.join(self.base_path, files[0])) as instance:
            lines = instance.readlines()
        # TODO: \n or other newline feed?
        return "\n".join(lines)


    ########################################################################
    ########################################################################
    ##########################  Dataset ##############################
    ########################################################################
    ########################################################################


    def add_dataset(self, dataset, message):
        """Register a dataset in the MathDataBase.
        It is added in the pending list waiting for approval by an editor.

        :param datastructure: A JSON object as a string
        :param message: A description of the dataset (the commit message)
        :returns: The name of the branch in which the dataset was commited"""
        # It stores datasets under the "datasets" path
        (self.base_path, available_repo_id) = self.get_available_repository()
        os.chdir(os.path.join(self.base_path, "dataset"))

        # Get the hash of the file
        process = Popen(["git", "hash-object", "--stdin", "--path", "dataset"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(dataset))[0]
        hash = stdo.decode()[:-1]

        # Create a new branch in the repo with name the hash of the datastructure
        subprocess.call(["git", "branch", hash])
        # TODO: Check if fail
        subprocess.call(["git", "checkout", hash])
        # TODO: Check if fail

        # Write the file
        with open(hash, 'w') as dataset_file:
            dataset_file.write(dataset)

        # Add and commit in the new branch
        subprocess.call(["git", "add", os.path.join(self.base_path, "dataset", hash) ])
        subprocess.call(["git", "commit", "-m", message])

        commit_hash = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:'%H'"]).decode()[:-1]


        # Add the branch name in the pending list at the default_branch.
        subprocess.call(["git", "checkout", self.definition["default_branch"]])

        # TODO: Check if fail
        with open(os.path.join(self.base_path, 'dataset_pending.txt'), 'a') as dataset_pending:
            dataset_pending.write(commit_hash+"\n")

        self.index_db.sql_add_commit(commit_hash, available_repo_id)
        return "ok"


    def approve_dataset(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        index_file_name = 'dataset_index.txt'

        self.remove_hash_from_pending(commit_hash, "dataset_pending.txt")

        # TODO: Not thread safe! Assumes we are in default_branch.
        subprocess.check_output(["git", "merge", "-m", message, commit_hash])

        # Add merge in index list
        with open(index_file_name, 'a') as dataset_index:
                dataset_index.write(commit_hash+"\n")

        # Commit the new index in the default_branch
        subprocess.check_output(["git", "add", os.path.join(self.base_path, index_file_name) ])
        subprocess.check_output(["git", "commit", "-m", "Merged dataset "+commit_hash])

        return 0

    def reject_dataset(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        self.remove_hash_from_pending(commit_hash,"dataset_pending.txt")


    def pending_datasets(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir(self.base_path)

        with open("dataset_pending.txt", "r") as dataset_pending:
            lines = dataset_pending.readlines()
        result = [ line.strip("'").strip("\n") for line in lines ]

        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.pending_datasets(step+1, repo_count)

        return result

    def get_datasets(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir(self.base_path)

        with open("dataset_index.txt", "r") as dataset_index:
            lines = dataset_index.readlines()
        result = [ line.strip("\n") for line in lines ]

        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.get_datasets(step+1, repo_count)
        return result

    def retrieve_dataset(self, hash):
        self.cd_to_commit_repository(hash)
        files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hash ]).decode()[:-1]
        files = files.split("\n")

        if len(files) == 0:
            return "0 files!"

        if len(files)>1:
            return "More than one files in the commit"

        with open(os.path.join(self.base_path, files[0])) as dataset:
            lines = dataset.readlines()
        # TODO: \n or other newline feed?
        return "\n".join(lines)


    ########################################################################
    ########################################################################
    ##########################  Format ##############################
    ########################################################################
    ########################################################################


    def add_format(self, formatjson, message):
        """Register a format in the MathDataBase.
        It is added in the pending list waiting for approval by an editor.

        :param format: A JSON object as a string
        :param message: A description of the dataset (the commit message)
        :returns: The name of the branch in which the dataset was commited"""
        (self.base_path, available_repo_id) = self.get_available_repository()
        os.chdir(os.path.join(self.base_path, "format"))

        # Get the hash of the file
        process = Popen(["git", "hash-object", "--stdin", "--path", "format"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(formatjson))[0]

        hash = stdo.decode()[:-1]

        # Create a new branch in the repo with name the hash of the datastructure
        subprocess.call(["git", "branch", hash])
        # TODO: Check if fail
        subprocess.call(["git", "checkout", hash])
        # TODO: Check if fail

        # Write the file
        with open(hash, 'w') as format_file:
            format_file.write(formatjson)

        # Add and commit in the new branch
        subprocess.call(["git", "add", os.path.join(self.base_path, "format", hash) ])
        subprocess.call(["git", "commit", "-m", message])


        commit_hash = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:'%H'"]).decode()[:-1]


        # Add the branch name in the pending list at the default_branch.
        subprocess.call(["git", "checkout", self.definition["default_branch"]])

        # TODO: Check if fail
        with open(os.path.join(self.base_path, 'format_pending.txt'), 'a') as format_pending:
            format_pending.write(commit_hash+"\n")

        self.index_db.sql_add_commit(commit_hash, available_repo_id)
        return commit_hash + " added."


    def approve_format(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        index_file_name = 'format_index.txt'

        self.remove_hash_from_pending(commit_hash, "format_pending.txt")

        # TODO: Not thread safe! Assumes we are in default_branch.
        subprocess.check_output(["git", "merge", "-m", message, commit_hash])

        # Add merge in index list
        with open(index_file_name, 'a') as format_index:
            format_index.write(commit_hash+"\n")

        # Commit the new index in the default_branch
        subprocess.check_output(["git", "add", os.path.join(self.base_path, index_file_name) ])
        subprocess.check_output(["git", "commit", "-m", "Merged dataset "+commit_hash])

        return 0

    def reject_format(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        self.remove_hash_from_pending(commit_hash, "format_pending.txt")


    def pending_formats(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir(self.base_path)

        with open("format_pending.txt", "r") as format_pending:
            lines = format_pending.readlines()
        result = [ line.strip("'").strip("\n") for line in lines ]

        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.pending_formats(step+1, repo_count)
        return result

    def get_formats(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )

        with open("format_index.txt", "r") as format_index:
            lines = format_index.readlines()
        result = [ line.strip("\n") for line in lines ]

        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.get_formats(step+1, repo_count)
        return result

    def retrieve_format(self, hash):
        self.cd_to_commit_repository(hash)
        files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hash ]).decode()[:-1]
        files = files.split("\n")

        if len(files) == 0:
            return "0 files!"

        if len(files)>1:
            return "More than one files in the commit"

        with open(os.path.join(self.base_path, files[0])) as format:
            lines = format.readlines()
        # TODO: \n or other newline feed?

        return "\n".join(lines)


    def get_formats_by_datastructure(self,datastructure, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )
        response = []
        with open("format_index.txt", "r") as index_file:
            keys = [str(line.strip("\n")) for line in index_file.readlines()]
            for key in keys:
                # To slow? Dont convert to json
                if json.loads(self.retrieve_format(key))["datastructure"] == datastructure:
                    response.append(key)
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            response += self.get_formats_by_datastructure(datastructure, step+1, repo_count)
        return response

    ########################################################################
    ########################################################################
    ##########################  Formatter  #################################
    ########################################################################
    ########################################################################


    def add_formatter(self, formatter_name, formatter, source_format, target_format,  message):
        """Register a formatter in the MathDataBase.
        It is added in the pending list waiting for approval by an editor.

        :param formatter: A python script formatting data from one format to another.
        :param source_format: The format of the input (given by the commit-hash of the format)
        :param target_format: The format of the outut (given by the commit-hash of the format)
        :returns: The name of the branch in which the formatter was commited"""
        # It stores formatters under the "formatter" path
        (self.base_path, available_repo_id) = self.get_available_repository()
        os.chdir(os.path.join(self.path,self.base_path,"formatter"))


        # Get the hash of the file
        process = Popen(["git", "hash-object", "--stdin", "--path", "formatter"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        stdo = process.communicate(input=str.encode(formatter))[0]
        hash = stdo.decode()[:-1]


        # Create a new branch in the repo with name the hash of the formatter
        subprocess.check_output(["git", "branch", hash]).decode()[:-1]
        # TODO: Check if fail
        subprocess.check_output(["git", "checkout", hash]).decode()[:-1]
        # TODO: Check if fail


        # Write the file
        with open(hash, 'w') as formatter_file:
            formatter_file.write(formatter)

        # Add and commit in the new branch
        subprocess.check_output(["git", "add", os.path.join(self.path,self.base_path,"formatter",hash) ]).decode()[:-1]
        subprocess.check_output(["git", "commit", "-m", message]).decode()[:-1]
        commit_hash = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:'%H'"]).decode()[:-1]


        # Add "from to branch name" in the pending list at the default_branch.
        subprocess.check_output(["git", "checkout", self.definition["default_branch"]]).decode()[:-1]
        # TODO: Check if fail

        with open(os.path.join(self.path,self.base_path,'formatter_pending.txt'), 'a') as formatter_pending:
            formatter_line = str(source_format) + " "
            formatter_line = formatter_line + str(target_format) + " "
            formatter_line = formatter_line + str(commit_hash.strip("'")) + " "
            formatter_line = formatter_line + str(formatter_name)
            formatter_line = formatter_line + "\n"
            formatter_pending.write(formatter_line)


        self.index_db.sql_add_commit(commit_hash, available_repo_id)
        # Return 0 on success
        return commit_hash + " added."


    def reject_formatter(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)
        source_format = ""
        targetnk_format = ""
        with open("formatter_pending.txt", "r") as formatter_pending:
            lines = formatter_pending.readlines()
        with open("formatter_pending.txt", "w") as formatter_pending:
            for line in lines:
                if line.strip("\n").split(" ")[2] != commit_hash:
                    formatter_pending.write(line.strip("\n") + "\n")
                else:
                    source_format = line.strip("\n").split(" ")[0]
                    target_format = line.strip("\n").split(" ")[1]


    def approve_formatter(self, commit_hash, message):
        self.cd_to_commit_repository(commit_hash)

        # Remove from pending list but keep from and to
        source_format = ""
        targetnk_format = ""
        with open("formatter_pending.txt", "r") as formatter_pending:
            lines = formatter_pending.readlines()
        with open("formatter_pending.txt", "w") as formatter_pending:
            for line in lines:
                if line.strip("\n").split(" ")[2] != commit_hash:
                    formatter_pending.write(line.strip("\n")+"\n")
                else:
                    source_format = line.strip("\n").split(" ")[0]
                    target_format = line.strip("\n").split(" ")[1]
                    formatter_name = line.strip("\n").split(" ")[3]

        # TODO: Not thread safe! Assumes we are in default_branch.
        subprocess.check_output(["git", "merge", "-m", message, commit_hash]).decode()[:-1]

        # Add merge in index list
        with open('formatter_index.txt', 'a') as formatter_index:
                formatter_index.write(source_format + " " + target_format + " " + commit_hash+ " " + formatter_name + "\n")
        # Commit the new index in the default_branch
        subprocess.check_output(["git", "add", os.path.join(self.path,self.base_path,'formatter_index.txt') ]).decode()[:-1]
        subprocess.check_output(["git", "commit", "-m", "Merged formatter "+commit_hash]).decode()[:-1]

        return 0

    def pending_formatters(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir(self.base_path)

        with open("formatter_pending.txt", "r") as formatter_pending:
            lines = formatter_pending.readlines()
        result = [ line.strip("\n").split(" ")[2] for line in lines ]
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.pending_formatters(step+1, repo_count)
        return result

    def get_formatters(self, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )

        with open("formatter_index.txt", "r") as formatter_index:
            lines = formatter_index.readlines()
        result = [ line.strip("\n") for line in lines ]
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.get_formatters(step+1, repo_count)
        return 

    def retrieve_formatter(self, hash):
        self.cd_to_commit_repository(hash)
        files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hash ]).decode()[:-1]
        files = files.split("\n")
        if len(files)>1:
            raise Exception("More than one files in the commit")
        with open(os.path.join(self.path,self.base_path, files[0])) as formatter:
            lines = formatter.readlines()
        # TODO: \n or other newline feed?
        return "\n".join(lines)


    def get_formatters_by_datastructure(self,datastructure, step=0, repo_count=0):
        formats = self.get_formats_by_datastructure(datastructure)
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )

        response = []
        with open("formatter_index.txt", "r") as index_file:
            lines = [str(line.strip("\n")) for line in index_file.readlines()]
            for line in lines:
                keys= line.split(" ")
                if keys[0] in formats:
                    response.append(keys)
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            response += self.get_formatters_by_datastructure(datastructure, step+1, repo_count)
        return response

    def get_formatters_by_format(self,format, step=0, repo_count=0):
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )
        response = []
        with open("formatter_index.txt", "r") as index_file:
            lines = [str(line.strip("\n")) for line in index_file.readlines()]
            for line in lines:
                keys= line.split(" ")
                if keys[0] == format:
                    response.append(line)
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            response += self.get_formatters_by_format(format, step+1, repo_count)
        return response


    def format_instance(self,instance, formatter):
        # Instance and formatter can be in different repositories, but retriever functions handle that case
        # By choice we commit result to instance's repository
        self.cd_to_commit_repository(instance)

        tmpfilename =  os.path.join(self.path,self.base_path,'scratch',instance+formatter+".py")
        outfilename =  os.path.join(self.path,self.base_path,'scratch',instance+formatter+".txt")
        with open(tmpfilename, "w") as tmp_file:
            tmp_file.write("input="+ self.retrieve_instance(instance))
            tmp_file.write("\n\n")
            tmp_file.write(self.retrieve_formatter(formatter))
            tmp_file.write("\n\n")
            tmp_file.write("with open(\""+ outfilename + "\", \"w\") as out_file:\n")
            tmp_file.write("    out_file.write(str(do_format(input)))")

        subprocess.check_output(["python3",tmpfilename])
        with open(outfilename, "r") as out_file:
            return out_file.read()


    ########################################################################
    ########################################################################
    ##########################  Batch operations ###########################
    ########################################################################
    ########################################################################


    def format_file(self,fname, from_format, to_format):
        os.chdir(self.base_path)

        # Find the correct formatter
        formatter=0
        for f in self.get_formatters():
            keys= f.split(" ")
            print(keys)

            if keys[0]==from_format and keys[1]==to_format:
                formatter=keys[2]
                break
        print("done with loop")

        if formatter==0:
            raise Exception("Formatter not found")
        print("about to create filename")

        tmpfilename =  os.path.join(self.path,self.base_path,'import_scratch',fname,fname+formatter+".py")
        outfilename =  os.path.join(self.path,self.base_path,'import_scratch',fname,fname+formatter+".txt")
        print(tmpfilename)
        print(outfilename)

        with open(tmpfilename, "w") as tmp_file:
            with open(os.path.join(self.path,self.base_path,'import_scratch',fname,fname), "r") as input_file:
                tmp_file.write("input="+ input_file.read() )
                tmp_file.write("\n\n")
                tmp_file.write(self.retrieve_formatter(formatter))
                tmp_file.write("\n\n")
                tmp_file.write("with open(\""+ outfilename + "\", \"w\") as out_file:\n")
                tmp_file.write("    out_file.write(str(format(input)))")

        subprocess.check_output(["python3",tmpfilename])
        with open(outfilename, "r") as out_file:
            self.add_instance(out_file.read(),"Imported")



    def import_dataset(self,fname, split_script, from_format, to_format):
        os.chdir(self.base_path)

        # Find the correct formatter
        formatter=0
        for f in self.get_formatters():
            keys= f.split(" ")
            print(keys)

            if keys[0]==from_format and keys[1]==to_format:
                formatter=keys[2]
                break
        print("done with loop")

        if formatter==0:
            raise Exception("Formatter not found")
        print("about to create filename")


        tarfilename=os.path.join(self.path,self.base_path,'import_scratch',fname,fname)
        tar = tarfile.open(name=tarfilename, mode='r')
        tarfolder =         tarfilename=os.path.join(self.path,self.base_path,'import_scratch',fname,"extract")
        tar.extractall(path=tarfolder)


        tmpfilename =  os.path.join(self.path,self.base_path,'import_scratch',fname,fname+formatter+".py")
        outfilename =  os.path.join(self.path,self.base_path,'import_scratch',fname,fname+formatter+".txt")
        print(tmpfilename)
        print(outfilename)

        with open(tmpfilename, "w") as tmp_file:
            with open(os.path.join(self.path,self.base_path,'import_scratch',fname,fname), "r") as input_file:
                tmp_file.write("input="+ input_file.read() )
                tmp_file.write("\n\n")
                tmp_file.write(self.retrieve_formatter(formatter))
                tmp_file.write("\n\n")
                tmp_file.write("with open(\""+ outfilename + "\", \"w\") as out_file:\n")
                tmp_file.write("    out_file.write(str(format(input)))")

        subprocess.check_output(["python3",tmpfilename])
        with open(outfilename, "r") as out_file:
            self.add_instance(out_file.read(),"Imported")


    ########################################################################
    ########################################################################
    ########################  Repository utils #############################
    ########################################################################
    ########################################################################

    def get_available_repository(self):
        """
        If repository is bloated, creates a new repository and returns its path, otherwise returns current repository.
        """
        lastCreatedRepositoryPath = self.index_db.sql_get_repository_address(self.index_db.sql_get_last_repository_id())
        lastCreatedRepositoryPath = os.path.join(self.path, lastCreatedRepositoryPath)
        du_result = subprocess.check_output(['du','-sh', lastCreatedRepositoryPath]).split()[0].decode('utf-8')
        byte_unit = du_result[-1]
        do_create_new_repository = False
        if byte_unit == 'M':
            # throw the size letter at the end
            size = int(du_result[0:-1].split('.')[0])
            if size >= self.MAX_REPOSITORY_SIZE_MB:
                do_create_new_repository = True
        elif byte_unit == 'G':
            do_create_new_repository = True
        if do_create_new_repository:
            current_repository_id = self.index_db.sql_get_last_repository_id()
            # Create repository directory
            repository_address = self.create_new_repository(current_repository_id+1)
            # Store directory of this repository in database
            self.index_db.sql_add_repository(repository_address)
        # if a new repository is created, sql_get_last_repository_id will return its id
        # otherwise it will return the already used repository
        available_repo_id = self.index_db.sql_get_last_repository_id()
        repository_folder = self.index_db.sql_get_repository_address(available_repo_id)
        result_folder = os.path.join(self.path, repository_folder)
        return (result_folder, available_repo_id)

    def create_new_repository(self,new_repository_id):
        new_repository_path = os.path.join(self.path, self.name)+str(new_repository_id)+".git"
        #os.mkdir(new_repository_path)
        self.init_and_set_directory(new_repository_path, self.mdb_def)
        return new_repository_path

    def get_commit_path(self,commit_hash):
        result = os.path.join(self.path, self.index_db.sql_get_address_from_commit(commit_hash))
        return result

    def cd_to_commit_repository(self,commit_hash):
        """
        Side effect: changes self.base_path
        """
        self.base_path = os.path.join(self.path,self.get_commit_path(commit_hash))
        os.chdir(self.base_path)