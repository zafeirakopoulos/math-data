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
        self.__current_repos = repo

    @property
    def instance_repo(self):
        return self.__instance_repo

    @instance_repo.setter
    def instance_repo(self, repo):
        self.__instance_repo = repo

    @property
    def next_file(self):
        return self.__next_file

    @next_file.setter
    def next_file(self, num):
        self.__next_file = num

    @property
    def instance_file(self):
        return self.__index_file

    @instance_file.setter
    def instance_file(self, filename):
        self.__instance_file = filename

    @property
    def index_file(self):
        return self.__index_file

    @index_file.setter
    def index_file(self, filename):
        self.__index_file = filename

    def __init__(self, basedir):

        self.__aspects = ["raw", "semantics", "typeset", "context", "features"]

        self.__current_repos = {self.aspects[0]: "repo1",
                                self.aspects[1]: "repo1",
                                self.aspects[2]: "repo1",
                                self.aspects[3]: "repo1",
                                self.aspects[4]: "repo1"}

        self.__instance_repo = "repo1"
        self.__instance_file = "1.txt"

        self.__index_file = "1.txt"

        self.__basedir = basedir

        self.__initial_setup()

        self.__next_file = \
            {self.aspects[0]:
                len(os.listdir(os.path.join(self.basedir, self.aspects[0], self.current_repos[self.aspects[0]]))),
             self.aspects[1]:
                 len(os.listdir(os.path.join(self.basedir, self.aspects[1], self.current_repos[self.aspects[1]]))),
             self.aspects[2]:
                 len(os.listdir(os.path.join(self.basedir, self.aspects[2], self.current_repos[self.aspects[2]]))),
             self.aspects[3]:
                 len(os.listdir(os.path.join(self.basedir, self.aspects[3], self.current_repos[self.aspects[3]]))),
             self.aspects[4]:
                 len(os.listdir(os.path.join(self.basedir, self.aspects[4], self.current_repos[self.aspects[4]])))
             }

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

    def get_last_sha(self, path, filename):
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
        """
        Initial setup of MDB.
        It creates files structure for MDB

        :return: None
        """

        for aspect in self.aspects:
            aspect_dir = os.path.join(self.basedir, aspect)

            # attributes directories creation
            if not os.path.exists(aspect_dir):
                os.makedirs(aspect_dir)

                # repo directories creation
                repo_dir = os.path.join(aspect_dir, self.current_repos[aspect])

                # repo creation
                if not os.path.exists(repo_dir):
                    self.__repo = Repo.init(repo_dir).git

        # Now part of instance and index

        json_array = []

        # instance part

        # instance file creation
        instance_dir = os.path.join(self.basedir, "instance")
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)

        # instance repo directory
        instance_repo_dir = os.path.join(instance_dir, self.instance_repo)
        if not os.path.exists(instance_repo_dir):
            self.__repo = Repo.init(instance_repo_dir).git

        # instance file creation
        instance_file = os.path.join(instance_repo_dir, self.instance_file)
        if not os.path.exists(instance_file):
            with open(instance_file, 'w') as outfile:
                json.dump(json_array, outfile)

        # index part

        # index directory creation
        index_dir = os.path.join(self.basedir, "index")
        if not os.path.exists(index_dir):
            self.__repo = Repo.init(index_dir).git

        # index file creation
        index_file = os.path.join(index_dir, self.index_file)
        if not os.path.exists(index_file):
            with open(index_file, 'w') as outfile:
                json.dump(json_array, outfile)

        return None

    def history_instance(self):
        pass

    def statistics(self):

        context_path = os.path.join(self.basedir, "context")

        instance = {}

        for repos in os.listdir(context_path):

            context_repo_path = os.path.join(self.basedir, "context", repos)

            for filename in os.listdir(context_repo_path):

                if filename == ".git":
                    continue

                with open(os.path.join(context_repo_path, filename), "r") as json_file:
                    datatype = json.load(json_file)

                if datatype in instance:
                    instance[datatype] += 1
                else:
                    instance[datatype] = 1

        return instance

    def definitions(self):
        """Return the list of all object definitions in the database.
        """
        return []

    def definition(self, key):
        """Return the definition corresponding to the given key.
        """
        return {}

    def status(self):
        """Return the current status of the database.
        """
        return 0

    def sanitize(self):
        """Sanitize the database.
        """
        return 0
