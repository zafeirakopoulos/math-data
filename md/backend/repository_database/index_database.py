import sqlite3 as sl
import os
from md.md_def import md_root

class IndexDatabase():
	"""
	TODO: sanitize queries against sql injection
	"""
	# If you change database_path, remember to add it to .gitignore
	database_path = os.path.join( os.path.join(md_root, "md/backend") ,"index_db.sqlite")

	# To explicitly indicate this is first initialization, call with initialize=True
	def __init__(self, initialize=False):
		if not os.path.isfile(self.database_path):
			initial = True
		else:
			initial = False
		# TODO: check if there is a chance for multithread issues occurring
		self.connection = sl.connect(self.database_path, check_same_thread=False)
		if initial:
			for query in self._initial_queries:
				retval = self.connection.execute(query)
	
	def sql_add_commit(self, commit_hash, repo_id):
		self.connection.execute("INSERT INTO commit_repositories (commit_hash, repo_id) values ('%s')" % (commit_hash))
		self.connection.commit()

	def sql_add_repository(self, address):
		self.connection.execute("INSERT INTO commit_repositories (address) values ('%s')" % (address))
		self.connection.commit()

	def get_repository_address(self, repo_id):
		self.connection.execute("SELECT address FROM commit_repositories WHERE id=%d" % (repo_id))
		self.connection.commit()

	def sql_remove_commit(self, commit_hash):
		self.connection.execute("DELETE FROM commit_repositories WHERE %s='%s'" % ("hash", commit_hash))
		self.connection.commit()

	def sql_get_last_repository_id():
		q = "SELECT MAX(id) from repositories);"

	# Queries to be executed at time of database creation
	_initial_queries = [
		"DROP TABLE IF EXISTS repositories;",
		"DROP TABLE IF EXISTS commit_repositories;",

		"""
		CREATE TABLE repositories(
			id integer PRIMARY KEY,
			address text
		);
		"""
	,
		"""
		CREATE TABLE commit_repositories(
			commit_hash text PRIMARY KEY,
			repo_id integer references repositories(id)
		);
		INSERT INTO repositories (id,address) values (0, 'localhost://mdbase.git')
		"""
	]
