import json

import git
from git import Repo
from os import makedirs, fsync
from os.path import exists, join
from uuid import uuid4
from base64 import urlsafe_b64decode, urlsafe_b64encode


# TODO Update documentation.
class Table:
    """A simple implementation of a DB Table using git as DB Manager."""
    def __init__(self, path):
        """Creates a table with given path.

        :param path: Path of the new table
        :returns: A Table instance"""
        # instead of being a repo, right now table is just a container folder.
        self.base = path
        self.sms = {}

        if not exists(path):
            makedirs(path)

        stat_file = join(path, "stats.json")

        if not exists(stat_file):
            # initial case the table is newly created and there is no stats.json file
            with open(stat_file, "w") as f:
                self.stat = {'active': None, 'insertions': 0, 'repos': []}  # This is the format of the file.
                self._create_subrepo_()
                json.dump(self.stat, f)
        else:
            with open(stat_file, "r") as f:
                self.stat = json.load(f)

    def _create_subrepo_(self, name=None):
        if name is None:
            name = str(uuid4())
        self.stat['active'] = name
        self.stat['insertions'] = 0
        self.stat['repos'].append(name)
        sm_path = join(self.base, name)
        Repo.init(sm_path).working_dir = sm_path

    def _get_repo_(self, name):
        if name not in self.sms:
            # The repo may not be accessed before.
            if name not in self.stat['repos']:
                # There is no repo like this
                return None, None
            path = join(self.base, name)
            self.sms[name] = {}
            self.sms[name]['repo'] = Repo(path)
            self.sms[name]['index'] = self.sms[name]['repo'].index
        return self.sms[name]['repo'], self.sms[name]['index']

    def add(self, content, msg, filename=None):
        """"Adds given file to the Table as a new entry with msg as the commit message.

        :param content: New entry content
        :param msg: Commit message.
        :param filename: Filename of the newly created entry.
        :returns: A JSON string with "success" and "sha" keys."""

        if filename is None:
            filename = str(uuid4())

        if self.stat['insertions'] == 100:
            self._create_subrepo_()
            self.stat['insertions'] = 0
        self.stat['insertions'] += 1
        self.save()

        repo, index = self._get_repo_(self.stat['active'])

        with open(join(repo.working_dir, filename), "w") as f:
            print(content, file=f)
            f.flush()
            fsync(f.fileno())
        repo.git.add(filename)
        sha = index.commit(msg).hexsha
        b64 = urlsafe_b64encode(("%s:%s" % (self.stat['active'], sha)).encode())
        return {"success": True, "sha": b64}

    def remove(self, b64, msg):
        """Removes a file from Table.

        :param sha: Last commit sha for file.
        :param msg: Commit message.
        :returns: A JSON file with "success" and "sha" keys."""
        sm, sha = urlsafe_b64decode(b64).decode().split(":")
        repo, index = self._get_repo_(sm)
        for filename in repo.commit(sha).stats.files.items():
            index.remove(filename, working_tree=True)
            sha = index.commit(msg).hexsha
            b64 = urlsafe_b64encode(("%s:%s" % (sm, sha)).encode())
            return {'success': True, "sha": b64}

        return {"success": False, "error": "something when wrong"}  # TODO add real error message

    # TODO deprecate this function, we dont need this one I think.
    def remove_file(self, filename):
        result = self.index.remove([filename], working_tree=True)
        sha = self.index.commit("").hexsha
        return {"success": len(result) == 1, "sha": sha}

    def update(self, b64, content, msg):
        """Updates a file from the Table.

        :param b64: Last commit sha for file.
        :param content: New content of the file.
        :param msg: Commit message.
        :returns: A JSON file with "success" and "sha" keys."""
        result = self.remove(b64)

        if not result['success']:
            return result

        result = self.add(content, msg)

        if not result['success']:
            return result

        return {"success": True, "sha": result['sha']}

    def __iter__(self):
        """Creates a generator based iterator over Table for entries."""
        for repo_path in self.stat['repos']:
            repo = Repo(repo_path)
            for commit in repo.iter_commits():
                yield """{"msg":"%s","sha":"%s"}""" % (commit.message, commit.hexsha)

    def get(self, b64):
        """Retrieves a file from Table with commit sha.

        :param sha: Commit sha.
        :returns: A stream to the content of the file."""
        return self[b64]

    def __getitem__(self, b64):
        """Retrieves a file from Table with commit sha.

        :param sha: Commit sha.
        :returns: A stream to the content of the file."""

        sm, sha = urlsafe_b64decode(b64).decode().split(":")

        repo, index = self._get_repo_(sm)
        commit = repo.commit(sha)

        for filename, _ in commit.stats.files.items():
            return filename, commit.tree[filename].data_stream.read()

        return None, None  # TODO return something meaningful, and discuss if this is meaningful enough

    def save(self):
        # Was a __del__ function before, and it was not working due to changes done after python 3.4
        # This is just a quick fix till I find a better way.
        stat_file = join(self.base, "stats.json")
        with open(stat_file, "w") as f:
            json.dump(self.stat, f)


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
