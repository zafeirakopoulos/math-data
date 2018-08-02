import os
import json
from git import Repo



class mdb:

    __repos = {}

    __file_number = {}
    __datatypes = []

    @property
    def aspects(self):
        return self.__aspects

    @aspects.setter
    def aspects(self, value):
        self.__aspects = value

    @property
    def basedir(self):
        return self.__basedir

    @basedir.setter
    def basedir(self, value):
        # Check if valid dirname
        self.__basedir = value

    @property
    def current_repos(self):
        return self.__current_repos

    @current_repos.setter
    def current_repos(self, repo):
        self.__current_repo = repo

    def __init__(self, basedir):

        self.__aspects = ["raw", "semantics", "typeset", "context", "features"]

        self.__current_repos = {self.aspects[0]: "repo1",
                                self.aspects[1]: "repo1",
                                self.aspects[2]: "repo1",
                                self.aspects[3]: "repo1",
                                self.aspects[4]: "repo1"
                                }

        self.__basedir = basedir
        self.__current_repo = "repo1"

        self.__initial_setup()

    def git_add(self, path, filename, message):
        """
        Add file to git

        :param path: that should has include .git
        :param filename: file name to add
        :param message: commit message
        :return: none
        """

        repo = Repo.init(path).git
        index = Repo(path).index

        # add file to repo
        repo.add(filename)
        index.commit(message)

    def git_remove(self, path, filename, message):
        """
        remove file from git

        :param path: that should has include .git
        :param filename: file name to remove
        :param message: commit message
        :return: none
        """

        index = Repo(path).index
        repo = Repo(path).git
        repo.rm(filename)

        index.commit(message)

    def get_attributes(self):
        return self.__attributes

    def get_basedir(self):
        return self.__basedir

    def get_file_number(self):
        return self.__file_number

    def get_last_sha(self,path, filename):
        """
        To get last commit sha key which we can access it permanently.
        :param path:
        :param filename:
        :return:
        """

        repo = Repo(path)
        commit = repo.head.commit

        return commit.hexsha

    def get_first_sha(self, path, filename):

        """ Private Helper Function.
        To get first commit sha key which we can access it permanently.
        :param path:
        :param filename:
        :return: firs commit sha key
        """

        repo = Repo(path)
        commits = list(repo.iter_commits('master', filename))
        commits.reverse()

        return commits[0].hexsha

    def __initial_setup(self):

        for aspect in self.aspects:
            aspect_dir = os.path.join(self.basedir, aspect)

            # attributes directories creation
            if not os.path.exists(aspect_dir):
                os.makedirs(aspect_dir)

                # repo directories creation
                repo_dir = os.path.join(aspect_dir, self.current_repos[aspect])
                if not os.path.exists(repo_dir):
                    self.__repo = Repo.init(repo_dir).git

        json_array = []

        # instance file creation
        instance_dir = os.path.join(self.basedir, "instance")
        if not os.path.exists(instance_dir):
            with open(instance_dir, 'w') as outfile:
                json.dump(json_array, outfile)

        # index file creation
        index_dir = os.path.join(self.basedir, "index")
        if not os.path.exists(index_dir):
            with open(index_dir, 'w') as outfile:
                json.dump(json_array, outfile)

        return None

    def history_instance(self):
        pass

    def statistics(self):

        with open(os.path.join(self.__basedir, "log.txt")) as json_file:
            dic = json.load(json_file)

        instance = {}

        for datatype in self.__datatypes:
            instance[datatype] = dic["remaining-" + datatype]

        return instance

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
