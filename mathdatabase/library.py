import os
from git import Repo

class Library:
    def create_commit(self, message):
    """Create a commit to the mathdatabse.
    It commits the current branch and creates a new one.
    """

    def merge_request(self, commitbranch, mainbranch="master"):
    """Push commits to the mathdatabse.
    All the commits in the commitbranch are pulled in the mainbranch.
    """
