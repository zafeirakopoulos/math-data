import json

from git import Repo
from os import makedirs, remove
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
        return '{"success":1,"sha":"%s"}' % self.index.commit(commit_msg).hexsha

    def remove(self, sha):
        commit_msg = json.loads(self.repo.git.execute(["git", "log", "--format=%B", "-n", "1", sha]))
        remove(join(self.repo.working_dir, commit_msg['file']))
        return '{"success":1,"sha":"%s"}' % self.index.commit("").hexsha

    def update(self, sha, file, msg):
        for commit in self.repo.iter_commits():
            if commit.hexsha != sha:
                continue

            commit_msg = json.loads(commit.message)
            copy(file, join(self.repo.working_dir, commit_msg['file']))
            commit_msg['msg'] = msg
            return '{"success":1,"sha":"%s"}' % self.index.commit(json.dumps(commit_msg)).hexsha
        return '{"success":0}'

    def get(self, sha):
        return self[sha]

    def __getitem__(self, sha):
        commit_msg = json.loads(self.repo.git.execute(["git", "log", "--format=%B", "-n", "1", sha]))
        return self.repo.git.execute(["git", "show", '%s:%s' % (sha, commit_msg['file'])])


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
