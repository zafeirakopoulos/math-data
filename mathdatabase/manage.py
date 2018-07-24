import os
import json
from git import Repo


class mdb:

    __attributes = ("raw", "semantics", "typeset", "context", "features", "index")
    __file_number = {}
    __current_path = ""
    __datatypes = []

    def __init__(self, datatypes, path):

        self.__initial_setup(datatypes=datatypes, path=path)
        self.__current_path = path
        self.__datatypes = datatypes

        dir_file = os.path.join(path, "log.txt")

        with open(dir_file) as json_file:
            self.__file_number = json.load(json_file)

    def get_attributes(self):
        return self.__attributes

    def get_current_path(self):
        return self.__current_path

    def get_file_number(self):
        return self.__file_number

    def get_sha(self, path, filename):

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

    def __initial_setup(self, datatypes, path):

        for datatype in datatypes:
            dir_datatype = os.path.join(path, datatype)

            if not os.path.exists(dir_datatype):
                os.makedirs(dir_datatype)

            for attribute in self.__attributes:
                dir_attribute = os.path.join(dir_datatype, attribute)

                if not os.path.exists(dir_attribute):
                    os.makedirs(dir_attribute)

                    dir_git = os.path.join(dir_attribute, ".git")

                    if not os.path.exists(dir_git):
                        repo = Repo.init(dir_attribute)

        dir_log = os.path.join(path, "log.txt")

        # create log.txt json
        if not os.path.exists(dir_log):
            dic = {}
            for key in datatypes:
                dic[key] = 0
                dic["remaining-" + key] = 0

            # write dic to log.txt
            with open(dir_log, 'w') as outfile:
                json.dump(dic, outfile)

        # if log.txt already exist
        # if new data type will be add, it should be add log.txt
        else:
            # read log.txt to dic
            with open(dir_log) as json_file:
                dic = json.load(json_file)

            # difference between new and old data types
            new_datatype = list(set(datatypes) - set(dic.keys()))

            if new_datatype:

                # add new data type log.txt
                dic[new_datatype[0]] = 0
                dic["remaining-" + new_datatype[0]] = 0

                # write all changed in log.txt
                with open(dir_log, 'w') as outfile:
                    json.dump(dic, outfile)

    def add_datatype(self, datatype):
        """
        This method add a new data type in working directory.
        You can add mdb constructor when you start your packet again

        :param datatype: data type
        :return: none
        """

        self.__file_number[datatype] = 0
        self.__file_number["remaining-" + datatype] = 0

        self.__datatypes.append(datatype)
        self.__initial_setup([datatype], self.__current_path)

    def history_instance(self):
        pass

    def statistics(self):

        with open(os.path.join(self.__current_path, "log.txt")) as json_file:
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
