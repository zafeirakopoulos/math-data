import os
import json
from git import Repo
from threading import Lock

mutex = Lock()


class math_data:

    __attributes = ("raw", "semantics", "typeset", "context", "features", "index")
    __file_number = {}
    __current_path = ""

    def __init__(self, datatypes, path):

        self.__initial_setup(datatypes=datatypes, path=path)
        self.__current_path = path

        dir_file = os.path.join(path, "log.txt")

        with open(dir_file) as json_file:
            self.__file_number = json.load(json_file)



    def __get_sha(self, path, filename):

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

    def __create_file(self, file_path, filename, content, dir_attribute, commit_message):

        """ Private Helper Function.
        Create a file that is specified with its file number.
        :param content: content of the marked file
        :param dir_attribute: path of the repo
        :param commit_message:
        :return: accessed repository sha key
        """
        # write file
        with open(file_path, 'w') as outfile:
            json.dump(content, outfile)
        repo = Repo.init(dir_attribute).git
        index = Repo(dir_attribute).index

        repo.add(filename)
        index.commit(commit_message)

        # get repo sha
        return self.__get_sha(path=dir_attribute, filename=filename)

    def __update_file(self, content, path, commit_message, filename):

        """Private Helper Function.
        Write new data to target file. Add repository with new commit message
        :param content: New content to edit target file
        :param path: repository path
        :param commit_message:
        :param filename:
        :return: none
        """
        repo = Repo(path).git
        index = Repo(path).index

        # generate path
        file_path = os.path.join(path, filename)

        # write target file
        with open(file_path, 'w') as outfile:
            json.dump(content, outfile)

        # add repo
        repo.add(filename)
        index.commit(commit_message)

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

        if not os.path.exists(dir_log):
            dic = {}
            for key in datatypes:
                dic[key] = 0

            with open(dir_log, 'w') as outfile:
                json.dump(dic, outfile)
        else:
            dic = {}
            with open(dir_log) as json_file:
                dic = json.load(json_file)

            new_datatype = list(set(datatypes) - set(dic.keys()))
            #  print(new_datatype)
            if new_datatype:

                dic[new_datatype[0]] = 0

                with open(dir_log, 'w') as outfile:
                    json.dump(dic, outfile)

    def __add_helper(self, data, sha_list):
        """ Private Helper Function.
        Go through target path and creates new data type
        :param data: incoming json file.
        :param sha_list: sha list of all attribute such as context
        :return: none
        """

        datatype = data["datatype"]

        if os.path.exists(datatype):

            self.__file_number[datatype] += 1

            filename = "file" + str(self.__file_number[datatype]) + ".txt"

            for attribute in self.__attributes:

                dir_attribute = os.path.join(self.__current_path, datatype, attribute)
                file_path = os.path.join(dir_attribute, filename)
                if os.path.exists(dir_attribute):
                    sha_list.append(self.__create_file(file_path, filename, data[attribute], dir_attribute, data["commit"]))

            # update log file according to data type
            dir_log = os.path.join(self.__current_path, "log.txt")
            with open(dir_log, 'w') as outfile:
                json.dump(self.__file_number, outfile)

        else:
            pass

    def add_instance(self, data):
        """
        It is dependent to name of data type.
        if new data type required to add new file structure is created.
        Otherwise, add just a new file.

        input example;

            r = {
                "datatype": "graph",   # may be polynomial
                "index": "index example",
                "raw": "raw example",
                "features": "features example",
                "semantics": "semantics example",
                "context":  {"edge": {"1": 100, "2": 2000},
                             "vertex": [{"first": 4, "second": 4},
                                        {"first": 3, "second": 55}]},
                "typeset": "typeset example",
                "commit": "update_repo"
            }


        return example;

            {sha : a63813d76910623f2b92ca7343682fe9ee2230a1 , 'status': 1}

            if removal is unsuccessful;

            {'status': 0} # this line will be rewrite


        :param data: incoming json file.
        :return: sha key of index of datatype.
        """
        sha_list = []

        mutex.acquire()
        try:
            self.__add_helper(data, sha_list)
        finally:
            mutex.release()

        status = 1  # will be fix

        response = {
            "sha": sha_list[len(sha_list)-1],    # index represent all of datatype to perform on it.
            "status": status                            # if successful otherwise 0
        }

        return response

    def remove_instance(self, data):
        """
        It is dependent to name of data type and its sha key.
        An example as fallow;

        input example;

            r = {
                "datatype": "graph",
                "sha": "a9f870b98077b86f4cff2afbb90c3255c8f9a923"
            }

            other example

            r = {
                "datatype": "polynomial",
                "sha": "12b8a0b98077b86f4cff2afbb90c3255c8f9affc"
            }

        return example;

            {'status': 1}

            if removal is unsuccessful;

            {'status': 0}

        :param data: incoming json file.
        :return: control status
        """
        status = 0
        datatype = data["datatype"]

        if os.path.exists(datatype):

            input_sha = data["sha"]

            dir_index = os.path.join(self.__current_path, datatype, "index")

            for filename in os.listdir(dir_index):

                # we ignore .git file
                if filename == ".git":
                    continue

                if input_sha == self.__get_sha(dir_index, filename):

                    for attribute in self.__attributes:

                        #file_path = os.path.join(os.path.curdir, datatype, attribute, filename)

                        path = os.path.join(self.__current_path, datatype, attribute)

                        index = Repo(path).index
                        repo = Repo(path).git
                        repo.rm(filename)

                        #os.remove(file_path)

                        index.commit("deleted repo")
                    status = 1

                    # decrease log file data type and write log again
                    self.__file_number[datatype] -= 1
                    with open(os.path.join(self.__current_path, "log.txt"), 'w') as outfile:
                        json.dump(self.__file_number, outfile)

                    break





        response = {
            "status": status  # if successful otherwise 0
        }

        return response

    def retrieve_instance(self, data):

        """ Fetches an instance which match with "input" sha key

        input example;

            r = {
                "datatype": "graph",
                "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
            }

            other example

            r = {
                "datatype": "polynomial",
                "sha": "21fa767a68101f4b7e75ffe50001954d0ee37a74"
            }

        return example;

            r = {
                "datatype": "graph",   # may be polynomial
                "index": "index example",
                "raw": "raw example",
                "features": "features example",
                "semantics": "semantics example",
                "context":  {"edge": {"1": 100, "2": 2000},
                             "vertex": [{"first": 4, "second": 4},
                                        {"first": 3, "second": 55}]},
                "typeset": "typeset example"
            }

        :param data: incoming json file.
        :return: desired instance
        """

        datatype = data["datatype"]

        response = {"datatype": datatype}

        status = -1

        if not os.path.exists(datatype):
            status = 0

        else:
            input_sha = data["sha"]

            dir_index = os.path.join(self.__current_path, datatype, "index")

            for filename in os.listdir(dir_index):

                if filename == ".git":
                    continue

                if input_sha == self.__get_sha(dir_index, filename):
                    for attribute in self.__attributes:
                        file_path = os.path.join(self.__current_path, datatype, attribute, filename)

                        with open(file_path) as json_file:
                            response[attribute] = json.load(json_file)

                    status = 1
                    break

        response["status"] = status

        return response

    def update_instance(self, data):
        """
        update instance which match with "input" sha key

        input example;

            r = {
                "datatype": "graph",   # may be polynomial
                "sha": "12b8a0b98077b86f4cff2afbb90c3255c8f9affc",
                "index": "index example",
                "raw": "raw example",
                "features": "features example",
                "semantics": "semantics example",
                "context":  {"edge": {"1": 100, "2": 2000},
                             "vertex": [{"first": 4, "second": 4},
                                        {"first": 3, "second": 55}]},
                "typeset": "typeset example",
                "commit": "update_repo"
            }


        return example;

            {'status': 1}

            if removal is unsuccessful;

            {'status': 0}

        :param data: incoming json file.
        :return:
        """

        datatype = data["datatype"]

        status = 0

        if not os.path.exists(datatype):
            status = 0

        else:
            input_sha = data["sha"]

            dir_index = os.path.join(self.__current_path, datatype, "index")

            for filename in os.listdir(dir_index):

                if filename == ".git":
                    continue

                if input_sha == self.__get_sha(dir_index, filename):
                    for attribute in self.__attributes:
                        dir_attribute = os.path.join(self.__current_path, datatype, attribute)

                        self.__update_file(data[attribute], dir_attribute, data["commit"], filename)
                    status = 1
                    break

        response = {
            "status": status  # if successful otherwise 0
        }

        return response

    def history_instance(self):
        print("")

    '''
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
    '''
