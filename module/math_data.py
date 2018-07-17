import os
import json
from git import Repo

class math_data:

    __attributes = ("raw", "semantics", "typeset", "context", "features", "index")

    def __get_sha(self, path, filename):

        repo = Repo(path)
        commits = list(repo.iter_commits('master', filename))
        commits.reverse()

        return commits[0].hexsha

    def __find_last_file_number(self, files):

        max_num = 0
        for filename in files:

            if filename == ".git":
                continue
            # 4 is number of file number char index
            if int(filename[4]) > max_num:
                max_num = int(filename[4])

        return max_num + 1

    # param : content  This
    # param : path
    # param : commit_massage
    def __create_file(self, content, path, commit_message):

        max_number = self.__find_last_file_number(os.listdir(path))
        filename = "file" + str(max_number) + ".txt"
        file_path = os.path.join(path, filename)

        # write file
        with open(file_path, 'w') as outfile:
            json.dump(content, outfile)

        found = 0
        for file in os.listdir(path):
            if file == ".git":
                found = 1
                break

        # add repo
        if found == 0:
            repo = Repo.init(path).git
            index = Repo(path).index
        else:
            repo = Repo(path).git
            index = Repo(path).index

        repo.add(filename)
        index.commit(commit_message)

        # get repo sha

        return self.__get_sha(path=path, filename=filename)

    def __update_file(self, content, path, commit_message, filename):

        repo = Repo(path).git
        index = Repo(path).index

        file_path = os.path.join(path, filename)

        with open(file_path, 'w') as outfile:
            json.dump(content, outfile)

        # add repo
        repo.add(filename)
        index.commit(commit_message)

    def __initial_setup(self, data, sha_list):

        datatype = data["datatype"]

        if not os.path.exists(datatype):
            os.makedirs(datatype)

        for attribute in self.__attributes:
            dir_attribute = os.path.join(os.path.curdir, datatype, attribute)

            if not os.path.exists(dir_attribute):
                os.makedirs(dir_attribute)
                sha_list.append(self.__create_file(data[attribute], dir_attribute, data["commit"]))


    def add_instance(self, data):

        sha_list = []
        self.__initial_setup(data, sha_list)

        status = 1

        response = {
            "sha": sha_list[len(sha_list)-1],    # index represent all of datatype to perform on it.
            "status": status                            # if successful otherwise 0
        }

        return response

    def remove_instance(self, data):

        status = 0
        datatype = data["datatype"]

        if os.path.exists(datatype):

            input_sha = data["sha"]

            dir_index = os.path.join(os.path.curdir, datatype, "index")

            for filename in os.listdir(dir_index):

                if filename == ".git":
                    continue
                print(input_sha, self.__get_sha(dir_index, filename))
                if input_sha == self.__get_sha(dir_index, filename):

                    for attribute in self.__attributes:
                        file_path = os.path.join(os.path.curdir, datatype, attribute, filename)
                        os.remove(file_path)
                        path = os.path.join(os.path.curdir, datatype, attribute)
                        index = Repo(path).index
                        index.commit("deleted repo")
                    status = 1
                    break

        response = {
            "status": status  # if successful otherwise 0
        }

        return response

    def retrieve_instance(self, data):

        datatype = data["datatype"]

        response = {"datatype": datatype}

        status = -1

        if not os.path.exists(datatype):
            status = 0

        else:
            input_sha = data["sha"]

            dir_index = os.path.join(os.path.curdir, datatype, "index")

            for filename in os.listdir(dir_index):

                print(filename)
                if filename == ".git":
                    continue

                if input_sha == self.__get_sha(dir_index, filename):
                    for attribute in self.__attributes:
                        file_path = os.path.join(os.path.curdir, datatype, attribute, filename)

                        with open(file_path) as json_file:
                            response[attribute] = json.load(json_file)

                    status = 1
                    break

        response["status"] = status

        return response

    def update_instance(self, data):

        datatype = data["datatype"]
        print(datatype)

        status = -1

        if not os.path.exists(datatype):
            status = 0

        else:
            input_sha = data["sha"]

            dir_index = os.path.join(os.path.curdir, datatype, "index")

            for filename in os.listdir(dir_index):

                print(filename)
                if filename == ".git":
                    continue

                if input_sha == self.__get_sha(dir_index, filename):
                    for attribute in self.__attributes:
                        dir_attribute = os.path.join(os.path.curdir, datatype, attribute)

                        self.__update_file(data[attribute], dir_attribute, data["commit"], filename)
                    status = 1
                    break

        response = {
            "status": status  # if successful otherwise 0
        }

        return response

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

    ##def retrieve_instance(self,data):

