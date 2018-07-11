import os
from git import Repo

class Manage:
    __sha_list = []

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
    
