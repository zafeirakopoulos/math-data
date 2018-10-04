import os
import json
from git import Repo

class SpaceTime:
    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self, value):
        # Check if valid url
        self.__url = value

    @property
    def revision(self):
        return self.__revision
    @revision.setter
    def revision(self, value):
        # Check if valid Repo
        self.__revision = value

    def __init__(self, url, revision):
        self.url = url
        self.revision = revision

    def json(self):
        return {
            "url" : self.url,
            "revision" : self.revision
        }
