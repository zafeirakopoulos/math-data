from git import Repo
from os import makedirs
from os.path import exists, join
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

    def add(self, content, msg, filename=str(uuid4())):
        """"Adds given file to the Table as a new entry with msg as the commit message.

        :param file: Path of the file to be added.
        :param msg: Commit message.
        :returns: A JSON string with "success" and "sha" keys."""
        with open(join(self.repo.working_dir, filename), "w") as f:
            f.write(content)
        self.repo.git.add(filename)
        sha = self.index.commit(msg).hexsha
        return {"success": True, "sha": sha}

    def remove(self, sha, msg):
        """Removes a file from Table.

        :param sha: Last commit sha for file.
        :param msg: Commit message.
        :returns: A JSON file with "success" and "sha" keys."""
        for filename in self.repo.commit(sha).stats.files.items():
            self.index.remove(filename, working_tree=True)
            sha = self.index.commit(msg).hexsha
            return {'success': True, "sha": sha}

        return {"success": False, "error": "something when wrong"}

    def remove_file(self, filename):
        result = self.index.remove([filename], working_tree=True)
        sha = self.index.commit("").hexsha
        return {"success": len(result) == 1, "sha": sha}

    def update(self, sha, content, msg):
        """Updates a file from the Table.

        :param sha: Last commit sha for file.
        :param file: Path to the new content of the file.
        :param msg: Commit message.
        :returns: A JSON file with "success" and "sha" keys."""
        result = self.remove(sha)

        if not result['success']:
            return result

        result = self.add(content, msg)

        if not result['success']:
            return result

        return {"success": True, "sha": result['sha']}

    def __iter__(self):
        """Creates a generator based iterator over Table for entries."""
        for commit in self.repo.iter_commits():
            yield """{"msg":"%s","sha":"%s"}""" % (commit.message, commit.hexsha)

    def get(self, sha):
        """Retrieves a file from Table with commit sha.

        :param sha: Commit sha.
        :returns: A stream to the content of the file."""
        return self[sha]

    def __getitem__(self, sha):
        """Retrieves a file from Table with commit sha.

        :param sha: Commit sha.
        :returns: A stream to the content of the file."""
        for filename, _ in self.repo.commit(sha).stats.files.items():
            return filename, self.repo.commit(sha).tree[filename].data_stream

        return None, None


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
