from git import Repo
from os import makedirs
from os.path import exists, join, splitext
from shutil import copy
from uuid import uuid4


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

    def add(self, table, file, msg):
        repo_path = join(self.base, table)

        if not exists(repo_path):
            makedirs(repo_path)

        if table not in self.tables:
            self.tables[table] = Repo.init(repo_path)

        repo = self.tables[table]
        uuid_file = uuid4().hex + splitext(file)[1]
        copy(file, join(repo_path, uuid_file))
        repo.git.add(uuid_file)
        repo.index.commit(msg)
        pass

    def remove(self, table, file):
        pass

    def update(self, table, file, msg):
        pass


if __name__ == '__main__':
    db = DB("../../../tests/benchmark/db")

    db.add('test', 'hello world.txt', 'hello world')
