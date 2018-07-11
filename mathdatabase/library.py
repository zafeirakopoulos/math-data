import os
from git import Repo

def create_commit(mdb,  message):
    """Create a commit to the mathdatabse.
    It commits the current branch and creates a new one.
    """

def merge_request(mdb,  commitbranch, mainbranch="master"):
    """Push commits to the mathdatabse.
    All the commits in the commitbranch are pulled in the mainbranch.
    """
