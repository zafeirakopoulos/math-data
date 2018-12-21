import json
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os


class MathDataBase:
    base_path = None
    name = None
    definition = None

    def __init__(self,path,name,definition):
        self.definition = definition
        self.name = name
        self.base_path = os.path.join(path, self.name)+".git"
        subprocess.call(["git", "init", "--bare", self.base_path])
        os.chdir(self.base_path)

    def add_data_to_repo(self, path, data):
        os.chdir(self.base_path)
        process = Popen(["git", "hash-object", "-w", "--stdin", "--path", path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdo = process.communicate(input=str.encode(data))[0]
        return stdo.decode()[:-1]

    def retrieve_data_from_repo(self,repo,key):
        os.chdir(self.base_path)
        return subprocess.check_output(["git", "cat-file", "-p", key]).decode()

    def add_data_to_database(self, data):
        os.chdir(self.base_path)
        for path in self.definition["paths"]:
            if path in data:
                data_key = self.add_data_to_repo(path, str(data[path]))
                subprocess.check_output(["git", "update-index", "--add", "--cacheinfo", "100644",data_key, path]).decode()
        return subprocess.check_output(["git", "write-tree"]).decode()[:-1]

    def approve_data(self,key, message):
        os.chdir(self.base_path)
        response = subprocess.check_output(["git", "commit-tree", key, "-m", message]).decode()[:-1]
        with open('mdb_index.txt', 'a') as mdb_index:
            mdb_index.write(response+'\n')
        return response

    def retrieve_data_from_database(self, key):
        response = []
        for path in self.definition["paths"]:
            try:
                response.append( '"'+path+'":'+subprocess.check_output(["git", "show", key+":"+path]).decode())
            except:
                pass
        return ",".join(response)

    def mdb_index(self):
        with open('mdb_index.txt', 'r') as mdb_index:
            return [ line for line in mdb_index]
