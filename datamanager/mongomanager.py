import pymongo
from datamanager.project import Project
from datamanager.filemanager import FileManager
from datamanager.databasemanager import DatabaseManager
from properties import always_write_to_disk, database_host_and_port

class MongoDBManager(DatabaseManager, FileManager):
	"""
	Class that implements a MongoDB manager. To use this class, you must first call the method
	initialize_write_to_disk, then optionally call any other method for writing data to
	disk, and finally call the method finalize_write_to_disk.
	"""
	def __init__(self):
		"""
		Initializes this DB manager.
		"""
		self.client = pymongo.MongoClient(database_host_and_port)
		self.db = self.client["jidata"]
		self.projects = self.db["projects"]
		self.issues = self.db["issues"]

	def initialize_write_to_disk(self, project_name):
		"""
		Initializes the writing of a project to disk. In the case of MongoDB, it does nothing.

		:param project_name: the name of the project.
		"""
		pass

	def read_project_from_disk(self, project_name):
		"""
		Reads a project from disk given the name of the project.

		:param project_name: the name of the project to be read from disk.
		:returns: an object of type Project.
		"""
		project = Project()
		project["info"] = self.projects.find_one({"project_name": project_name})
		project["issues"] = {obj["_id"]: obj for obj in self.issues.find({"project_name": project_name})}
		return project

	def project_exists(self, project_name):
		"""
		Check if a project exists in the disk given the name of the project. The
		existence of the project is determined by whether it has an info.json file.

		:param project_name: the name of the project to be read from disk.
		:returns: True if the project exists, or False otherwise.
		"""
		return self.projects.find_one({"project_name": project_name})

	def finalize_write_to_disk(self, project_name, project):
		"""
		Finalizes the writing of a project to disk. Closes any open buffers.

		:param project_name: the name of the project to be written to disk.
		:param project: the project data to be written to disk.
		"""
		if not always_write_to_disk:
			project["info"]["_id"] = project["info"]["id"]
			project["info"]["project_name"] = project_name
			self.projects.update_one({"_id": project["info"]["_id"]}, {"$set": project["info"]}, upsert = True)
			for issue in project["issues"].values():
				issue["_id"] = issue["id"]
				issue["project_name"] = project_name
			self.update_multiple(self.issues, project["issues"].values(), upsert = True)

	def write_project_info_to_disk(self, project_name, info):
		"""
		Writes the info of a project to disk.

		:param project_name: the name of the project.
		:param info: the info to be written to disk.
		"""
		if always_write_to_disk:
			info["_id"] = info["id"]
			info["project_name"] = project_name
			self.projects.update_one({"_id": info["_id"]}, {"$set": info}, upsert = True)

	def write_project_issue_to_disk(self, project_name, issue):
		"""
		Writes an issue of a project to disk.

		:param project_name: the name of the project.
		:param issue: the issue to be written to disk.
		"""
		if always_write_to_disk:
			issue["_id"] = issue["id"]
			issue["project_name"] = project_name
			self.issues.update_one({"_id": issue["_id"]}, {"$set": issue}, upsert = True)
