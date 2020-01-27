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
    already_exists = False

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

        print("donnne")
        # Return 0 on success
        return "ok"


    def approve_datastructure(self, commit_hash, message):
        os.chdir(self.base_path)

        self.remove_hash_from_pending(commit_hash)

        # TODO: Not thread safe! Assumes we are in default_branch.
        subprocess.check_output(["git", "merge", "-m", message, commit_hash])

        # Add merge in index list
        with open('datastructure_index.txt', 'a') as datastructure_index:
                datastructure_index.write(commit_hash+"\n")

        # Commit the new index in the default_branch
        subprocess.check_output(["git", "add", os.path.join(self.base_path, 'datastructure_index.txt') ])
        subprocess.check_output(["git", "commit", "-m", "Merged datastructure "+commit_hash])

        return 0

    def reject_datastructure(self, commit_hash, message):
        os.chdir(self.base_path)
        self.remove_hash_from_pending(commit_hash)

    def get_diff(self, commit_hash):
        diff = subprocess.check_output(["git", "show", commit_hash]).decode()[:-1]
        return diff


    def pending_datastructures(self):
        os.chdir(self.base_path)

        with open("datastructure_pending.txt", "r") as datastructure_pending:
            lines = datastructure_pending.readlines()
        return [ line.strip("'").strip("\n") for line in lines ]

    def get_datastructures(self):
        os.chdir(self.base_path)

        with open("datastructure_index.txt", "r") as datastructure_index:
            lines = datastructure_index.readlines()
        return [ line.strip("\n") for line in lines ]

    def retrieve_datastructure(self, hash):
        files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hash ]).decode()[:-1]
        files = files.split("\n")

        if len(files) == 0:
            return "0 files!"

        if len(files)>1:
            return "More than one files in the commit"

        print(files[0])
        with open(os.path.join(self.base_path, files[0])) as datastructure:
            lines = datastructure.readlines()
        # TODO: \n or other newline feed?
        return "\n".join(lines)


    def remove_hash_from_pending(self, commit_hash):
        # Remove from pending list
        with open("datastructure_pending.txt", "r") as datastructure_pending:
            lines = datastructure_pending.readlines()
        with open("datastructure_pending.txt", "w") as datastructure_pending:
            for line in lines:
                if line.strip("'").strip("\n") != commit_hash:
                    datastructure_pending.write(line.strip("'").strip("\n")+"\n")

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

#        json.loads(

        # Split the raw data in the instance to be stored
        # Raw data are stored as git object to remove redundancy
        # It stores raw data under the "data" path
        os.chdir(os.path.join(mdb_root,self.base_path,"data"))
        hashes = {}
        raw = instance["raw"]
        if type(raw) is dict:
            for elt in raw:
                raw[elt]
        else:
            process = Popen(["git", "hash-object", "-w", "--stdin", "--path", "data"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            stdo = process.communicate(input=str.encode(raw))[0]
            hashes = stdo.decode()[:-1]


        # It stores instance under the "instance" path
        os.chdir(os.path.join(mdb_root,self.base_path,"instance"))

        # Get the hash of the file

        process = Popen(["git", "hash-object", "-w", "--stdin", "--path", path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(data))[0]
        hash =  stdo.decode()[:-1]



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


    def add_formatter(self, formatter, from, to,  message):
        """Register a formatter in the MathDataBase.
        It is added in the pending list waiting for approval by an editor.

        :param formatter: A python script formatting data from one format to another.
        :param from: The format of the input (given by the commit-hash of the format)
        :param from: The format of the outut (given by the commit-hash of the format)
        :returns: The name of the branch in which the formatter was commited"""
        # It stores formatters under the "formatter" path
        os.chdir(os.path.join(mdb_root,self.base_path,"formatter"))

        # Get the hash of the file
        process = Popen(["git", "hash-object", "--stdin", "--path", "formatter"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(formatter+from+to))[0]
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
        subprocess.check_output(["git", "add", os.path.join(mdb_root,self.base_path,"formatter",hash) ]).decode()[:-1]
        subprocess.check_output(["git", "commit", "-m", message]).decode()[:-1]
        commit_hash = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:'%H'"]).decode()[:-1]


        # Add "from to branch name" in the pending list at the default_branch.
        subprocess.check_output(["git", "checkout", self.definition["default_branch"]]).decode()[:-1]
        # TODO: Check if fail
        with open(os.path.join(mdb_root,self.base_path,'formatter_pending.txt'), 'a') as formatter_pending:
            formatter_pending.write(from + " " + to + " " +commit_hash.strip("'") +"\n")

        # Return 0 on success
        return 0


    def approve_formatter(self, commit_hash, message):
        os.chdir(os.path.join(mdb_root,self.base_path))

        # Remove from pending list but keep from and to
        from = ""
        to = ""
        with open("formatter_pending.txt", "r") as formatter_pending:
            lines = formatter_pending.readlines()
        with open("formatter_pending.txt", "w") as formatter_pending:
            for line in lines:
                if line.strip("\n").split(" ")[2] != commit_hash:
                    formatter_pending.write(line.strip("\n")+"\n")
                else:
                    from = line.strip("\n").split(" ")[0]
                    to = line.strip("\n").split(" ")[1]

        # TODO: Not thread safe! Assumes we are in default_branch.
        subprocess.check_output(["git", "merge", "-m", message, commit_hash]).decode()[:-1]

        # Add merge in index list
        with open('formatter_index.txt', 'a') as formatter_index:
                formatter_index.write(from + " " + to + " " + commit_hash+"\n")
        # Commit the new index in the default_branch
        subprocess.check_output(["git", "add", os.path.join(mdb_root,self.base_path,'formatter_index.txt') ]).decode()[:-1]
        subprocess.check_output(["git", "commit", "-m", "Merged formatter "+commit_hash]).decode()[:-1]

        return 0

    def pending_formatters(self):
        os.chdir(os.path.join(mdb_root,self.base_path))

        with open("formatter_pending.txt", "r") as formatter_pending:
            lines = formatter_pending.readlines()
        return [ line.strip("\n") for line in lines ]

    def get_formatters(self):
        os.chdir(os.path.join(mdb_root,self.base_path))

        with open("formatter_index.txt", "r") as formatter_index:
            lines = formatter_index.readlines()
        return [ line.strip("\n") for line in lines ]

    def retrieve_formatter(self, hash):
        files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hash ]).decode()[:-1]
        files = files.split("\n")
        if len(files)>1:
            raise Exception("More than one files in the commit")
        with open(os.path.join(mdb_root,self.base_path, files[0])) as formatter:
            lines = formatter.readlines()
        # TODO: \n or other newline feed?
        return "\n".join(lines)

    def retrieve_formatter_for(self, from):
        formatter_lines = []
        with open("formatter_index.txt", "r") as formatter_index:
            lines = formatter_index.readlines()
        for line in lines:
            if line.split(" ")[0]==hash:
                formatter_lines.append(line)
        # return pairs [output format, formatter]
        return [ [formatter[1], retrieve_formatter(formatter[2])] formatter in formatter_lines ]
