from mdb.data.db import DB, Table
import os
import json

class Index():

    @property
    def path(self):
        """
        :returns: The path of the index.
        """
        return self.__path

    @property
    def name(self):
        """
        :returns: Name of the index.
        """
        return self.__name

    @property
    def data(self):
        """
        :returns: The index dictionary.
        """
        return self.__data


    def __init__(self, path):
        self.__name = "Generic Index"
        self.__path = path
        self.__data = new Table(self.path())


    def __getitem__(self,keyword):
        """
        :returns: A list of keys for files relevant for keyword.
        """
        return self.data()[keyword]

    def add_entry(self,keyword,key):
        """
        Add or update an entry to the index: {keyword: [..., key]}

        :returns: 0 if fail, 1 if add, 2 if update.
        """


class TypeIndex(Index):

    __init__(self,name):
        super(TypeIndex, self).__init__()
