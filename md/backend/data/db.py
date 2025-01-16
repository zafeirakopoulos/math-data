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
        If no definition is given, it will return an existing MathDataBase.

        :param path: Path of the new MathDataBase in the filesystem
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
        """Initializes and configures the directory for the MathDataBase.

        Sets up a Git repository at the specified path, initializes files and folders,
        and configures the repository with the provided database definition.

        :param base_path: Path to the Git repository directory.
        :param mdb_def: (Optional) JSON string containing the MathDataBase definition."""

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
        """Removes a commit hash from the specified pending file.
        Reads the pending file, removes the specified hash, and updates the file.

        :param commit_hash: The commit hash to remove from the pending list.
        :param pending_file_name: Name of the pending file to modify."""
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
        """Approves a datastructure by merging its commit into the default branch and updating the index.
        Removes the commit hash from the pending list, merges it, and logs it in the datastructure index.

        :param commit_hash: The commit hash of the datastructure to approve.
        :param message: The commit message for the merge operation."""
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
        """Rejects a datastructure by removing its commit hash from the pending list.

        :param commit_hash: The commit hash of the datastructure to reject.
        :param message: The reason for rejecting the datastructure (not used in the function)."""
        self.cd_to_commit_repository(commit_hash)
        self.remove_hash_from_pending(commit_hash,"datastructure_pending.txt")


    def get_diff(self, commit_hash):
        """Fetches the diff of the specified commit hash.

        :param commit_hash: The commit hash to fetch the diff for.
        :returns: The diff showing changes introduced by the specified commit."""
        self.cd_to_commit_repository(commit_hash) #
        diff = subprocess.check_output(["git", "show", commit_hash]).decode()[:-1]
        return diff


    def pending_datastructures(self, step=0, repo_count=0):
        """Retrieves the list of pending datastructures across multiple repositories.

        Reads the 'datastructure_pending.txt' file in each repository and accumulates the pending datastructure commit hashes.

        :param step: The current repository step to start from (default is 0).
        :param repo_count: The total number of repositories to check (default is 0).
        :returns: A list of pending datastructure commit hashes."""
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
        """Retrieves the list of datastructures across multiple repositories.

        Reads the 'datastructure_index.txt' file in each repository and accumulates the datastructure commit hashes.

        :param step: The current repository step to start from (default is 0).
        :param repo_count: The total number of repositories to check (default is 0).
        :returns: A list of datastructure commit hashes."""
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
        """Retrieves the content of the datastructure file from the specified commit hash.

        This method uses the `git diff-tree` command to identify the modified file in the commit
        and reads its content. If there are no files or multiple files, appropriate messages are returned.

        :param hash: The commit hash to retrieve the datastructure from.
        :returns: The content of the datastructure file, or a message if no file or more than one file is found."""
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
        """Approves and merges an instance commit into the repository.

        Merges the specified commit into the default branch, removes it from the pending list,
        and updates the index file with the commit hash.

        :param commit_hash: The commit hash of the instance to approve.
        :param message: The commit message for the merge.
        :returns: 0 if successful."""
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
        """Rejects an instance commit by removing it from the pending list.

        Removes the specified commit hash from the pending list, indicating rejection.

        :param commit_hash: The commit hash of the instance to reject.
        :param message: The commit message for rejection (not used in the function)."""
        self.cd_to_commit_repository(commit_hash)
        self.remove_hash_from_pending(commit_hash,"instance_pending.txt")

    def pending_instances(self, step=0, repo_count=0):
        """Retrieves the list of pending instances from all repositories.

        Reads the 'instance_pending.txt' file in each repository and returns the commit hashes of pending instances.

        :param step: The current repository step to process (default is 0).
        :param repo_count: The total number of repositories to process (default is 0).
        :returns: A list of commit hashes for pending instances."""
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
        """Retrieves the list of instances from all repositories.

        Reads the 'instance_index.txt' file in each repository and returns the commit hashes of instances.

        :param step: The current repository step to process (default is 0).
        :param repo_count: The total number of repositories to process (default is 0).
        :returns: A list of commit hashes for instances."""
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
        """Retrieves the list of instances associated with a specific datastructure from all repositories.

        Checks each instance's datastructure and returns the commit hashes of instances that match the specified datastructure.

        :param datastructure: The datastructure to filter instances by.
        :param step: The current repository step to process (default is 0).
        :param repo_count: The total number of repositories to process (default is 0).
        :returns: A list of commit hashes for instances that match the specified datastructure."""
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
        """Retrieves the instance data for a specific commit hash.

        Fetches the file associated with the commit hash and returns its content. 
        If more than one file is found in the commit, an error message is returned.

        :param hash: The commit hash to retrieve the associated instance.
        :returns: The content of the file in the commit or an error message if no file or multiple files are found."""
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

        :param dataset: A list of hashes of instances
        :param message: A description of the dataset (the commit message)
        :returns: The name of the branch in which the dataset was commited"""
        # It stores datasets under the "datasets" path
        (self.base_path, available_repo_id) = self.get_available_repository()
        os.chdir(os.path.join(self.base_path, "dataset"))

        # Join hashes into a string seperated with newlines
        dataset_as_string = '\n'.join(dataset)
        # Get the hash of the file
        process = Popen(["git", "hash-object", "--stdin", "--path", "dataset"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(dataset_as_string))[0]
        hash = stdo.decode()[:-1]

        # Create a new branch in the repo with name the hash of the datastructure
        subprocess.call(["git", "branch", hash])
        # TODO: Check if fail
        subprocess.call(["git", "checkout", hash])
        # TODO: Check if fail

        # Write the file
        with open(hash, 'w') as dataset_file:
            dataset_file.write(dataset_as_string)

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
        """Approves and merges a dataset commit.

        Merges the dataset commit into the current branch, removes it from the pending list, 
        and updates the dataset index file with the commit hash. The changes are then committed.

        :param commit_hash: The commit hash of the dataset to approve.
        :param message: The commit message for the merge.
        :returns: 0 on success."""
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
        """Rejects a dataset commit and removes it from the pending list.

        The specified dataset commit is removed from the list of pending commits
        for the dataset, indicating that the dataset will not be approved.

        :param commit_hash: The commit hash of the dataset to reject.
        :param message: A message describing the reason for rejecting the dataset."""
        self.cd_to_commit_repository(commit_hash)
        self.remove_hash_from_pending(commit_hash,"dataset_pending.txt")


    def pending_datasets(self, step=0, repo_count=0):
        """Retrieves the list of pending datasets from the dataset_pending file.
    
        The method reads the 'dataset_pending.txt' file and compiles a list of 
        commit hashes for datasets that are pending approval. It recursively 
        processes the repositories if there are more than one.

        :param step: The current step/repository index for recursive processing.
        :param repo_count: The total number of repositories to process.
        :returns: A list of commit hashes for pending datasets."""
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
        """Retrieves the list of datasets from the dataset_index file.
    
        The method reads the 'dataset_index.txt' file and compiles a list of 
        commit hashes for datasets. It recursively processes the repositories 
        if there are more than one.

        :param step: The current step/repository index for recursive processing.
        :param repo_count: The total number of repositories to process.
        :returns: A list of commit hashes for datasets."""
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
        """Retrieves the dataset associated with a given commit hash.

        The method checks the files in the specified commit and returns the 
        contents of the dataset file, which is expected to be a single file in 
        the commit. If no file or more than one file is found, appropriate messages 
        are returned. The contents of the file are returned as a comma-separated 
        string with newlines removed.

        :param hash: The commit hash to retrieve the dataset for.
        :returns: The contents of the dataset file as a comma-separated string, 
                or a message indicating no files or multiple files in the commit."""
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
        #return "\n".join(lines)
        return ",".join(lines).replace('\n','')


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
        """Approves and merges a format commit.

        Merges the format commit into the current branch, removes it from the pending list,
        and updates the format index file with the commit hash. The changes are then committed.

        :param commit_hash: The commit hash of the format to approve.
        :param message: The commit message for the merge.
        :returns: 0 on success. """
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
        """Rejects a format commit.

        Removes the format commit from the pending list.

        :param commit_hash: The commit hash of the format to reject.
        :param message: The rejection message(not used in the function).
        :returns: None."""
        self.cd_to_commit_repository(commit_hash)
        self.remove_hash_from_pending(commit_hash, "format_pending.txt")


    def pending_formats(self, step=0, repo_count=0):
        """Retrieves a list of pending format commits.

        Reads the "format_pending.txt" file and retrieves the commit hashes of the pending formats. It recursively checks all repositories if necessary.

        :param step: The current repository step(default is 0).
        :param repo_count: The total number of repositories (default is 0).
        :returns: A list of commit hashes from the pending formats.
        """
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
        """Retrieves a list of format commit hashes.

        Reads the "format_index.txt" file and retrieves the commit hashes of the formats. It recursively checks all repositories if necessary.

        :param step: The current repository step(default is 0).
        :param repo_count: The total number of repositories (default is 0).
        :returns: A list of commit hashes from the format index."""
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
        """Retrieves the content of a format commit.

        Fetches the content of the format file associated with the provided commit hash. It checks the number of files in the commit and returns the content of the format file if only one file exists.

        :param hash: The commit hash of the format.
        :returns: The content of the format file.
        """
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
        """Retrieves format commit hashes by datastructure.

        Reads the "format_index.txt" file and retrieves the commit hashes of formats matching the specified datastructure. 
        It recursively checks all repositories if necessary.

        :param datastructure: The datastructure to filter by.
        :param step: The current repository step (default is 0).
        :param repo_count: The total number of repositories (default is 0).
        :returns: A list of commit hashes that match the specified datastructure.
        """
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
        """Rejects a formatter commit.

        todo

        :param commit_hash: The commit hash of the formatter to reject.
        :param message: The reason for rejecting the formatter.(not used in the function)"""
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
        """Approves and merges a formatter commit.

        Merges the given commit into the current branch and removes it from the pending list.
        Updates the formatter index with the source and target formats. The changes are then committed.

        :param commit_hash: The commit hash of the formatter to approve.
        :param message: The commit message for the merge.
        :returns: 0 on success."""
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
        """Retrieves a list of pending formatter commit hashes.

        Reads the "formatter_pending.txt" file and retrieves the commit hashes of the pending formatters. 
        It checks all repositories if necessary.

        :param step: The current repository step (default is 0).
        :param repo_count: The total number of repositories (default is 0).
        :returns: A list of commit hashes from the pending formatter list.
        """
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
        """Retrieves a list of formatter commit hashes.

        Reads the "formatter_index.txt" file and retrieves the commit hashes of the formatters. 
        It checks all repositories if necessary.

        :param step: The current repository step (default is 0).
        :param repo_count: The total number of repositories (default is 0).
        :returns: A list of commit hashes from the formatter index.
        """
        self.base_path = os.path.join(self.path, self.index_db.sql_get_repository_address(step))
        os.chdir( self.base_path )

        with open("formatter_index.txt", "r") as formatter_index:
            lines = formatter_index.readlines()
        result = [ line.strip("\n") for line in lines ]
        if repo_count == 0:
            repo_count = self.index_db.sql_get_last_repository_id()
        if step < repo_count:
            result += self.get_formatters(step+1, repo_count)
        return result

    def retrieve_formatter(self, hash):
        """Retrieves the content of a formatter file from a commit.

        Given a commit hash, this method checks for the modified files in the commit and reads the content of the related formatter file. 
        If more than one file is changed in the commit, an exception is raised.

        :param hash: The commit hash.
        :returns: The content of the formatter file.
        :raises Exception: If more than one file is modified in the commit.
        """
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
        """Retrieves formatters by datastructure type.

        This method iterates over repositories and retrieves formatter information from the 
        "formatter_index.txt" file for formatters that match the given datastructure.

        :param datastructure: The datastructure type to filter formatters by.
        :param step: The current repository step (default is 0).
        :param repo_count: The total number of repositories (default is 0).
        :returns: A list of formatters that match the given datastructure.
        """
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
        """Retrieves formatters by format type.

        This method iterates over repositories and retrieves formatter information from 
        the "formatter_index.txt" file for formatters that match the given format type.

        :param format: The format type to filter formatters by.
        :param step: The current repository step (default is 0).
        :param repo_count: The total number of repositories (default is 0).
        :returns: A list of formatters that match the given format type.
        """
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
        """Formats an instance using the specified formatter.

        This method writes a temporary Python script to apply the given formatter on 
        the provided instance. The script is then executed, and the result is saved 
        in a text file. The output is returned as the content of the result file.

        :param instance: The instance to be formatted.
        :param formatter: The formatter to apply to the instance.
        :returns: The result of the formatted instance.
        """
        # Instance and formatter can be in different repositories, but retriever functions handle that case
        # By choice we commit result to instance's repository
        self.cd_to_commit_repository(instance)
        print("hello")
        print("Instance ==>",instance)
        print("retrived instance:",self.retrieve_instance(instance))
        namespace = {}
        exec(self.retrieve_formatter(formatter), namespace)
        
        result = namespace['formatter'](json.loads(str(self.retrieve_instance(instance))))
        return result


    ########################################################################
    ########################################################################
    ##########################  Batch operations ###########################
    ########################################################################
    ########################################################################

    """Formats a file using the specified formats.

    This method reads the input file, applies the corresponding formatter (based on 
    the provided from_format and to_format), and writes the result to an output file. 
    It then adds the formatted output as an instance.

    :param fname: The name of the file to format.
    :param from_format: The format of the input file.
    :param to_format: The target format to apply.
    :raises Exception: If no matching formatter is found."""
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

        # .tpy is to prevent flask from tracking change and resetting while debug mode is on
        tmpfilename =  os.path.join(self.base_path,'import_scratch',fname,fname+formatter+".py")
        outfilename =  os.path.join(self.base_path,'import_scratch',fname,fname+formatter+".txt")
        print("Formatter: "+formatter)
        print("tmpfilename: "+tmpfilename)
        print("outfilename: "+outfilename)
        with open(tmpfilename, "w") as tmp_file:
            with open(os.path.join(self.base_path,'import_scratch',fname,fname), "r") as input_file:
                tmp_file.write("input=" + "\"" +input_file.read()+ "\"")
                tmp_file.write("\n\n")
                tmp_file.write(self.retrieve_formatter(formatter))
                tmp_file.write("\n\n")
                tmp_file.write("with open(\""+ outfilename + "\", \"w\") as out_file:\n")
                tmp_file.write("    out_file.write(str(do_format(input)))")

        subprocess.check_output(["python3",tmpfilename])
        with open(outfilename, "r") as out_file:
            self.add_instance(out_file.read(),"Imported")


    def import_instances(self,datastructure,file, from_format, to_format):
        """Imports and formats instances using the specified formats.

        This method extracts a dataset from a tar file, applies the corresponding formatter 
        (based on the provided from_format and to_format), and writes the result to an output 
        file. It then adds the formatted output as an instance.

        :param file: The file of the instances.
        :param datastructure: The datastructure of the instances.
        :param from_format: The format of the input dataset.
        :param to_format: The target format to apply.
        :raises Exception: If no matching formatter is found."""
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

        content = file.read()
        
        namespace = {}
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        exec(self.retrieve_formatter(formatter), namespace)
        result = namespace['formatter'](content)
        for instance in result:
            instance["datastructure"] = datastructure
            self.add_instance(json.dumps(instance),"Imported")

    # def import_dataset(self,fname, split_script, from_format, to_format):
    #     """Imports and formats a dataset using the specified formats.

    #     This method extracts a dataset from a tar file, applies the corresponding formatter 
    #     (based on the provided from_format and to_format), and writes the result to an output 
    #     file. It then adds the formatted output as an instance.

    #     :param fname: The name of the dataset to import.
    #     :param split_script: The script used for splitting the dataset (currently not used in the code).
    #     :param from_format: The format of the input dataset.
    #     :param to_format: The target format to apply.
    #     :raises Exception: If no matching formatter is found."""
    #     os.chdir(self.base_path)

    #     # Find the correct formatter
    #     formatter=0
    #     for f in self.get_formatters():
    #         keys= f.split(" ")
    #         print(keys)

    #         if keys[0]==from_format and keys[1]==to_format:
    #             formatter=keys[2]
    #             break
    #     print("done with loop")

    #     if formatter==0:
    #         raise Exception("Formatter not found")
    #     print("about to create filename")

    #     exec(self.retrieve_formatter(formatter))

    #     formatter()

        # tarfilename=os.path.join(self.path,self.base_path,'import_scratch',fname,fname)
        # tar = tarfile.open(name=tarfilename, mode='r')
        # tarfolder =         tarfilename=os.path.join(self.path,self.base_path,'import_scratch',fname,"extract")
        # tar.extractall(path=tarfolder)


        # tmpfilename =  os.path.join(self.path,self.base_path,'import_scratch',fname,fname+formatter+".py")
        # outfilename =  os.path.join(self.path,self.base_path,'import_scratch',fname,fname+formatter+".txt")
        # print(tmpfilename)
        # print(outfilename)

        # with open(tmpfilename, "w") as tmp_file:
        #     with open(os.path.join(self.path,self.base_path,'import_scratch',fname,fname), "r") as input_file:
        #         tmp_file.write("input="+ input_file.read() )
        #         tmp_file.write("\n\n")
        #         tmp_file.write(self.retrieve_formatter(formatter))
        #         tmp_file.write("\n\n")
        #         tmp_file.write("with open(\""+ outfilename + "\", \"w\") as out_file:\n")
        #         tmp_file.write("    out_file.write(str(format(input)))")

        # subprocess.check_output(["python3",tmpfilename])
        # with open(outfilename, "r") as out_file:
        #     self.add_instance(out_file.read(),"Imported")


    ########################################################################
    ########################################################################
    ########################  Repository utils #############################
    ########################################################################
    ########################################################################

    def get_available_repository(self):
        """ Checks the current repository size and decides whether to create a new repository 
        or return the existing one. If the current repository exceeds the maximum size, 
        a new repository is created. Otherwise, the path to the current repository is returned.

        :returns: A tuple containing the path to the available repository and its ID."""
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
        """ Creates a new repository directory and initializes it as a Git repository.
    
        :param new_repository_id: The ID to assign to the new repository.
        :returns: The path to the newly created repository."""
        new_repository_path = os.path.join(self.path, self.name)+str(new_repository_id)+".git"
        #os.mkdir(new_repository_path)
        self.init_and_set_directory(new_repository_path, self.mdb_def)
        return new_repository_path

    def get_commit_path(self,commit_hash):
        """ Returns the file path for the given commit hash.
    
        :param commit_hash: The commit hash to retrieve the path for.
        :returns: The file path for the specified commit hash."""
        result = os.path.join(self.path, self.index_db.sql_get_address_from_commit(commit_hash))
        return result

    def cd_to_commit_repository(self,commit_hash):
        """ Changes the current directory to the repository of the given commit hash.
    
        Side effect: Modifies the self.base_path and changes the current working directory to the commit's repository.
        
        :param commit_hash: The commit hash to change to the corresponding repository."""
        self.base_path = os.path.join(self.path,self.get_commit_path(commit_hash))
        os.chdir(self.base_path)