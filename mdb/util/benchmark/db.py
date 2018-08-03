from git import Repo
from os import makedirs
from os.path import exists, join, splitext
from shutil import copy
from uuid import uuid4
import git


class Table:
    def __init__(self, path):
        self.repo = Repo.init(path)
        self.repo.working_dir = path
        self.index = self.repo.index

    def add(self, file, msg):
        uuid_file = str(uuid4()) + splitext(file)[1]
        copy(file, join(self.repo.working_dir, uuid_file))
        self.repo.git.add(uuid_file)
        commit_msg = '{"file":"%s","msg":"%s"}' % (uuid_file, msg)
        return self.index.commit(commit_msg).hexsha

    def remove(self, sha):
        # TODO stub code
        return True

    def update(self, sha, file, msg):
        # TODO stub code
        return uuid4().hex

    def get(self, sha):
        # TODO stub code
        return self[sha]

    def __getitem__(self, sha):
        # TODO stub code
        with open('test_file1.json', 'r') as f:
            return f.read()


class DB:
    def __init__(self, path):
        self.__base = path
        self.__tables = {}
        if not exists(path):
            makedirs(path)
        pass

    @property
    def base(self):
        return self.__base

    @property
    def tables(self):
        return self.__tables

    def get(self, table):
        return self.__getitem__(table)
        pass

    def __getitem__(self, table):
        if table not in self.tables:
            self.tables[table] = Table(join(self.base, table))
        return self.tables[table]
