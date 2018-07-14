import os
import json
from git import Repo

class math_data:
    __sha_list = []
    __status = 0
    __attributes = ("raw", "semantics", "typeset", "context", "features", "index")

    def __get_sha(self, path, filename):

        repo = Repo(path)
        commits = list(repo.iter_commits('master', filename))
        commits.reverse()

        return commits[0].hexsha

    def __find_last_file_number(self, files):

        max_num = 1
        for filename in files:

            if filename == ".git":
                continue
            # 5 is number of file number char index
            if int(filename[4]) > max_num:
                max_num = int(filename[4])

        return max_num + 1

    def __create_file(self, content, path, commit_message):

        repo = Repo.init(path).git
        index = Repo.init(path).index
        max_number = self.__find_last_file_number(os.listdir(path))
        filename = "file" + str(max_number) + ".txt"
        file_path = os.path.join(path, filename)

        with open(file_path, 'w') as outfile:
            json.dump(content, outfile)
        # fill in the file
        #f = open(file_path, "w")
        #f.write(content)
        #f.close()

        # add repo
        repo.add(filename)
        index.commit(commit_message)

        # get repo sha
        self.__sha_list.append(self.__get_sha(path=path, filename=filename))

    def __initial_setup(self, data):

        datatype = data["datatype"]

        if not os.path.exists(datatype):
            os.makedirs(datatype)

        for attribute in self.__attributes:
            dir_attribute = os.path.join(os.path.curdir, datatype, attribute)

            if not os.path.exists(dir_attribute):
                os.makedirs(dir_attribute)
            self.__create_file(data[attribute], dir_attribute, data["commit"])

    def add_instance(self, data):
        self.__initial_setup(data)
        self.__status = 1
        print(self.__sha_list)
        response = {
            "sha": self.__sha_list[len(self.__sha_list)-1],    # index represent all of datatype to perform on it.
            "status": self.__status                            # if successful otherwise 0
        }
        self.__sha_list = []
        return response

    def remove_instance(self, data):

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
                        index = Repo.init(path).index
                        index.commit("deleted repo")
                    self.__status = 1
                    break

        else:
            self.__status = 0

        response = {
            "status": self.__status  # if successful otherwise 0
        }

        return response

    def retrieve_instance(self,data):
        print("")

    def update_instance(self,data):
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