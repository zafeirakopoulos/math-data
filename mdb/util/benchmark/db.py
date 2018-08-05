import json

from git import Repo
from os import makedirs, remove
from os.path import exists, join, splitext
from shutil import copy
from uuid import uuid4


class Table:
    """A simple implementation of a DB Table using git as DB Manager."""
    def __init__(self, path):
        """Creates a table with given path.

        :param path: Path of the new table
        :returns: A Table instance"""
        self.repo = Repo.init(path)
        self.repo.working_dir = path
        self.index = self.repo.index

    def add(self, file, msg):
        """"Adds given file to the Table as a new entry with msg as the commit message.

        :param file: Path of the file to be added.
        :param msg: Commit message.
        :returns: A JSON string with "success" and "sha" keys."""
        uuid_file = str(uuid4()) + splitext(file)[1]
        copy(file, join(self.repo.working_dir, uuid_file))
        self.repo.git.add(uuid_file)
        commit_msg = '{"file":"%s","msg":"%s"}' % (uuid_file, msg)
        return '{"success":1,"sha":"%s"}' % self.index.commit(commit_msg).hexsha

    def remove(self, sha):
        """Removes a file from Table.

        :param sha: Last commit sha for file.
        :returns: A JSON file with "success" and "sha" keys."""
        commit_msg = json.loads(self.repo.git.execute(["git", "log", "--format=%B", "-n", "1", sha]))
        remove(join(self.repo.working_dir, commit_msg['file']))
        return '{"success":1,"sha":"%s"}' % self.index.commit("").hexsha

    def update(self, sha, file, msg):
        """Updates a file from the Table.

        :param sha: Last commit sha for file.
        :param file: Path to the new content of the file.
        :param msg: Commit message.
        :returns: A JSON file with "success" and "sha" keys."""
        for commit in self.repo.iter_commits():
            if commit.hexsha != sha:
                continue

            commit_msg = json.loads(commit.message)
            copy(file, join(self.repo.working_dir, commit_msg['file']))
            commit_msg['msg'] = msg
            return '{"success":1,"sha":"%s"}' % self.index.commit(json.dumps(commit_msg)).hexsha
        return '{"success":0}'

    def get(self, sha):
        """Retrieves a file from Table with given sha.

        :param sha: Commit sha of the file.
        :returns: File content"""
        return self[sha]

    def __getitem__(self, sha):
        """Retrieves a file from Table with given sha.

        :param sha: Commit sha of the file.
        :returns: File content."""
        commit_msg = json.loads(self.repo.git.execute(["git", "log", "--format=%B", "-n", "1", sha]))
        return self.repo.git.execute(["git", "show", '%s:%s' % (sha, commit_msg['file'])])


class DB:
    """A simple DataBase using git as DB Manager."""
    def __init__(self, path):
        """Creates a DB with given path as base for storage.

        :param path: Base path of the DB.
        :returns: An DB instance."""
        self.__base = path
        self.__tables = {}
        if not exists(path):
            makedirs(path)
        pass

    @property
    def base(self):
        """
        :returns: Path of the DB.
        """
        return self.__base

    @property
    def tables(self):
        """Returns the tables active in this database. This is for internal use only."""
        return self.__tables

    def get(self, table):
        """Retrieve a Table from database.

        :param table: Name of the table.
        :returns: A Table instance."""
        return self.__getitem__(table)
        pass

    def __getitem__(self, table):
        """Retrieve a Table from database.

        :param table: Name of the table.
        :returns: A Table instance."""
        if table not in self.tables:
            self.tables[table] = Table(join(self.base, table))
        return self.tables[table]
