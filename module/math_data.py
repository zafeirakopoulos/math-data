import os
import json
from git import Repo


class math_data:
    __sha_list = []
    __status = 1


    def __get_sha(self, path, filename):

        repo = Repo(path)
        commits = list(repo.iter_commits('master', filename))
        commits.reverse()

        return commits[0].hexsha

    def __create_file(self, content, path, commit_message):

        repo = Repo.init(path).git
        index = Repo.init(path).index

        filename = "file" + str(len(os.listdir(path))) + ".txt"
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

        attributes = ("raw", "semantics", "typeset", "context", "features", "index")

        datatype = data["datatype"]

        if not os.path.exists(datatype):
            os.makedirs(datatype)

        for attribute in attributes:
            dir_attribute = os.path.join(os.path.curdir, datatype, attribute)

            if not os.path.exists(dir_attribute):
                os.makedirs(dir_attribute)
            self.__create_file(data[attribute], dir_attribute, data["commit"])

    def add_instance(self, data):
        self.__initial_setup(data)
        response = {
            "sha": self.__sha_list[len(self.__sha_list)-1],    # index represent all of datatype to perform on it.
            "status": self.__status                            # if successful otherwise 0
        }

        return response

    def remove_instance(self,data):


        print("")

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