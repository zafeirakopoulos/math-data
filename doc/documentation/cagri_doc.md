This document is about contents of branch "emekcagri".

# Multi repository support
There is now multi git repository support added in db.py.
If a repository size exceeds MAX_REPOSITORY_SIZE_MB in db.py, a new repository with folder name as mdbase+(id of new repository)+.git is automatically created (for example, mdbase1.git), and new commits are made on that git repository, the old ones arent used for adding anymore commits. 
At deployment, MAX_REPOSITORY_SIZE_MB has to be changed to desired size (right now it is 3mb for testing).

# Notes on changes

index_database.py
===================
This file contains sqlite operations to store the MathDatabase related data. There are two sql tables:

repositories
------------
This contains id and address of a git repository. The address is currently a directory path, it was called "address" because it was meant to support remote repositories too, this is still a TODO.

commit_repositories:
------------
This stores which commit hash belongs to which repository.

Currently there is no live running SQLite server, database queries are done on a file on disk, that file is index_db.sqlite, stored in the root folder.

# Notes on multi-repo support
If you need to test or use multi repository support, but **if you already have a MathDatabase created in your local git repo**, you have to synchronize with index_database.sqlite, which requires you to **delete mdbase.git** before starting the server, so that they sqlite database could initialize together with git repository. Because the added code in db.py creates the sqlite database by checking if mdbase.git repository does not exists.

# Possible bugs
If a bug similar to entities not appearing on menus or dropdowns occur, it might be because of some retriever functions are called in wrong order and switched to different repository by changing directory, and didnt change back. For example, in get_formatters_by_datastructure, function get_formats_by_datastructure is called. This fetches formats from all repos hence changes the directory to last repo and this resulted in formatters being fetched only from last repository (but this is currently fixed).