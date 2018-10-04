import os
import json
from git import Repo

class Instance:

    @property
    def raw(self):
        return self.__raw
    @raw.setter
    def raw(self, value):
        # Check if valid SpaceTime
        self.__raw = value

    @property
    def semantics(self):
        return self.__semantics
    @semantics.setter
    def semantics(self, value):
        # Check if valid SpaceTime
        self.__semantics = value

    @property
    def typeset(self):
        return self.__typeset
    @typeset.setter
    def typeset(self, value):
        # Check if valid SpaceTime
        self.__typeset = value

    @property
    def context(self):
        return self.__context
    @context.setter
    def context(self, value):
        # Check if valid SpaceTime
        self.__context = value

    @property
    def features(self):
        return self.__features
    @features.setter
    def features(self, value):
        # Check if valid SpaceTime
        self.__features = value


    def __init__(self, raw=None, semantics=None, typeset=None, context=None, features=None, key=None):
        if key == None:
            self.raw = raw
            self.semantics = semantics
            self.typeset = typeset
            self.context = context
            self.features = features


    def json(self):
        return {
            "raw" : self.raw.json(),
            "semantics" : self.semantics.json(),
            "typeset" : self.typeset.json(),
            "context" : self.raw.context(),
            "features" : self.features.json()
        }
