import sqlite3 as sl
import os
from md.md_def import md_root

class IndexDatabase():
	"""
	TODO: sanitize queries against sql injection
	"""
	# To explicitly indicate this is first initialization, call with initialize=True
	def __init__(self, path, name, initialize=False):
		"""
		:param name: Name of the MathDataBase that uses this API. Will indicate repository folder name
		"""
		# If you change database_path, remember to add it to .gitignore
		self.database_path = os.path.join( path, "index_db.sqlite")
		self.path = path
		if initialize or (not os.path.isfile(self.database_path)):
			initial = True
		else:
			initial = False
		# TODO: check if there is a chance for multithread issues occurring
		self.connection = sl.connect(self.database_path, check_same_thread=False)
		if initial:
			queries = self._generate_initial_queries(name)
			for query in queries:
				retval = self.connection.execute(query)
			# save changes to disk
			self.connection.commit()
	
	def sql_add_commit(self, commit_hash, repo_id):
		# a dirty hack: somethings are parsed incorrectly in db.py, so we fix here
		commit_hash = commit_hash.strip("'")
		self.connection.execute("INSERT INTO commit_repositories (commit_hash, repo_id) values ('%s', %d);" % (commit_hash, repo_id))
		self.connection.commit()

	def sql_add_repository(self, address):
		self.connection.execute("INSERT INTO repositories (address) values ('%s');" % (address))
		self.connection.commit()

	def sql_get_repository_address(self, repo_id):
		sql_result = self.connection.execute("SELECT address FROM repositories WHERE id=%d;" % (repo_id))
		return sql_result.fetchone()[0]

	def sql_set_repository_address(self, repo_id, new_address):
		self.connection.execute("UPDATE repositories SET address='%s' WHERE id=%d;" % (new_address, repo_id))
		self.connection.commit()

	def sql_remove_commit(self, commit_hash):
		# same hack as above
		ommit_hash = commit_hash.strip("'")		
		self.connection.execute("DELETE FROM commit_repositories WHERE commit_hash='%s';" % (commit_hash))
		self.connection.commit()

	def sql_get_address_from_commit(self, commit_hash):
		"""
		Returns the address of the git repository that this commit resides in
		"""
		sub_query	= "SELECT repo_id FROM commit_repositories WHERE commit_hash='%s'" % commit_hash
		query		= "SELECT address FROM repositories WHERE id=(%s)" % (sub_query)
		sql_result	= self.connection.execute(query)
		# fetchall returns a list of tuples, each tuple corresponding to a column
		fetched = sql_result.fetchall()
		if len(fetched) == 0:
			raise Exception("No commit %s in repositories database" % commit_hash)
		result = fetched[0][0]
		return result

	def sql_get_last_repository_id(self):
		return self.connection.execute("SELECT MAX(id) from repositories;").fetchone()[0]

	# Queries to be executed at time of database creation
	def _generate_initial_queries(self, name):
		initial_queries = [
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
			"""
			,
			"""
			INSERT INTO repositories (id,address) values (0, '%s.git')
			""" % name
		]
		return initial_queries
