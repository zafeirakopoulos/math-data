import os
from git import Repo
import hashlib

class MDB:
    __attributes = ("raw", "semantics", "typeset", "context", "features")
    __repos = {}
    ############################################################################
    ############################################################################
    ###  Functions to initialize and delete database
    ############################################################################
    ############################################################################
    def __init__(self, basedir, datatype,debug=False):
        datatypepath = os.path.join(basedir,datatype)
        # Check if the folder for the datatype already exists
        for file in os.listdir(basedir):
            datatype_exists = False
            if file == datatype:
                datatype_exists = True
                # The datatype folder exists
                is_git = False
                for file2 in os.listdir(datatypepath):
                    # if it is a git repo, just return it
                    if file2 == ".git":
                        if debug: print("Folder exists and is git initialized")
                        self.__repo = Repo(datatypepath).git
                        self.__index = Repo(datatypepath).index
                        if debug: print("Datatype exists and repository is initialized")
                        is_git = True
                        break
                if not is_git:
                    # If the folder is not a git repo, then initialize it
                    if debug: print("Folder exists but not git initialized")
                    self.__repo = Repo.init(datatypepath).git
                    self.__index = Repo(datatypepath).index
                    if debug: print("Initialized datatype: " + datatype)
                break
        # If the folder does not exist
        if not datatype_exists:
            if debug: print("Folder does not exist")
            os.makedirs(datatypepath)
            self.__repo = Repo.init(datatypepath).git
            self.__index = Repo(datatypepath).index
            if debug: print("Created folder and initialized datatype: " + datatype)

        # Now we have to check or create the repos.

        # We want to ingore these folders because they are repos themselves and
        # they are tracked separately
        #First check the .gitignore for the folders
        hasher = hashlib.md5()
        if os.path.exists(os.path.join(datatypepath,".gitignore")):
            with open(os.path.join(datatypepath,".gitignore"), 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
            if hasher.hexdigest()!="8f0b9d7f9079e1a2433447b16731cf86":
                raise Exception(".gitignore not ok")
        else:
            # TODO Create the .gitignore
            if debug: print(".gitignore does not exist. I will create it")
            file = open(os.path.join(datatypepath,".gitignore"),"w")
            for attribute in self.__attributes:
                file.write(attribute)
            file.close()
            self.__repo.add(os.path.join(datatypepath,".gitignore"))
            self.__index.commit("commit .gitignore for datatype " + datatype)


        if not os.path.exists(os.path.join(datatypepath,"index")):
            open(os.path.join(datatypepath,"index"), 'a').close()
            self.__repo.add(os.path.join(datatypepath,"index"))
            self.__index.commit("commit index for datatype " + datatype)


        # Now check the 5 repos
        for attribute in self.__attributes:
            attribute_path = os.path.join(datatypepath,attribute)
            # Check if the folder for the datatype already exists
            for file in os.listdir(datatypepath):
                attribute_exists = False
                if file == attribute:
                    attribute_exists = True
                    # The datatype folder exists
                    is_git = False
                    for file2 in os.listdir(attribute_path):
                        # if it is a git repo, just return it
                        if file2 == ".git":
                            if debug: print("Folder exists and is git initialized")
                            self.__repos[attribute] = Repo(attribute_path).git
                            if debug: print("Attribute exists and repository is initialized")
                            is_git = True
                            break
                    if not is_git:
                        # If the folder is not a git repo, then initialize it
                        if debug: print("Folder exists but not git initialized")
                        self.__repos[attribute] = Repo.init(attribute_path).git
                        if debug: print("Initialized attribute: " + attribute)
                    break
            # If the folder does not exist
            if not attribute_exists:
                if debug: print("Folder does not exist")
                os.makedirs(attribute_path)
                self.__repos[attribute] = Repo.init(attribute_path).git
                if debug: print("Created folder and initialized attribute: " + attribute)

        if debug: print(self.__repos)
        return None

    def __get_sha(self, path):

        master = Repo(path).head.reference

        return master.commit.hexsha

    def __create_file(self, filename,repo_content,commit_message):

        path = '.'
        repo = Repo.init(path).git
        index = Repo.init(path).index

        # fill in the file
        f = open(filename, "w")
        f.write(repo_content)
        f.close()

        # add repo
        repo.add(filename)
        index.commit(commit_message)

        # get repo sha

        self.__sha_list.append(self.__get_sha(path=path))

    def initial_setup(self, datatype, content):

        repos = ("raw", "semantics", "typeset", "context", "features", "index")
        try:
            os.makedirs(datatype)
            os.chdir(datatype)
            for repo in repos:
                os.makedirs(repo)
                os.chdir(repo)
                self.__create_file("file1.txt", content[repo], content["commit"])
                os.chdir("..")
            os.chdir("..")
            return self.__sha_list
        except OSError as e:
            raise ValueError('Cannot create! ', e.filename, ' is already exist')

    def log_repo(self, datatype, repo):
        r = Repo('graph/features').git
        print(r.log(p=True))

    def edit_repo(self, datatype, repo, sha, commit):

        os.chdir(datatype)
        os.chdir(repo)

        os.open("file1.txt", os.O_CREAT)

    def list_repo(self,datatype, repo, sha):

        os.chdir(datatype)
        os.chdir(repo)

        actual_sha = self.__get_sha(path='.')

        if actual_sha == sha:
            f = open("file1.txt", "r")
            repo_content = f.read()
            f.close()
            os.chdir("..")
            os.chdir("..")
            return repo_content
        else:
            os.chdir("..")
            os.chdir("..")
            return ""

    def definitions(self):
        """Return the list of all object definitions in the mathdatabase.
        """
        return []


    def definition(self, key):
        """Return the definition corresponding to the given key.
        """
        return {}

    def status(self):
        """Return the current status of the mathdatabase.
        """
        return 0


    def sanitize(self):
        """Sanitize the mathdatabase.
        """
        return 0

    def statistics(self):
        """Return a set of statistics about the mathdatabase.
        """
        return {"instances":2000}
