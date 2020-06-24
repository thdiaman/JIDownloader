import os
from datamanager.project import Project
from datamanager.filemanager import FileManager
from properties import dataFolderPath, always_write_to_disk

class DBManager(FileManager):
	"""
	Class that implements a DB manager. To use this class, you must first call the method
	initialize_write_to_disk, then optionally call any other method for writing data to
	disk, and finally call the method finalize_write_to_disk.
	"""
	def __init__(self):
		"""
		Initializes this DB manager.
		"""
		self.create_folder_if_it_does_not_exist(dataFolderPath)

	def initialize_write_to_disk(self, project_name):
		"""
		Initializes the writing of a project to disk. Creates all the necessary directories.

		:param project_name: the name of the project to be written to disk.
		"""
		rootfolder = os.path.join(dataFolderPath, project_name)
		self.create_folder_if_it_does_not_exist(rootfolder)
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues"))

	def read_project_from_disk(self, project_name):
		"""
		Reads a project from disk given the name of the project that is also the folder
		of the project.

		:param project_name: the name of the project to be read from disk.
		:returns: an object of type Project.
		"""
		project = Project()
		rootfolder = os.path.join(dataFolderPath, project_name)
		project["info"] = self.read_json_from_file_if_it_exists(os.path.join(rootfolder, "info.json"))
		project["issues"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issues"), "id")
		return project

	def project_exists(self, project_name):
		"""
		Check if a project exists in the disk given the name of the project that is also the folder
		of the project. The existence of the project is determined by whether it has an info.json file.

		:param project_name: the name of the project to be read from disk.
		:returns: True if the project exists, or False otherwise.
		"""
		return os.path.exists(os.path.join(dataFolderPath, project_name, "info.json"))

	def finalize_write_to_disk(self, project_name, project):
		"""
		Finalizes the writing of a project to disk. Closes any open buffers.

		:param project_name: the name of the project to be written to disk.
		:param project: the project data to be written to disk.
		"""
		if not always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, project_name)
			self.write_json_to_file(os.path.join(rootfolder, "info.json"), project["info"])
			for issue in project["issues"].values():
				self.write_json_to_file(os.path.join(rootfolder, "issues", str(issue["id"]) + ".json"), issue)

	def write_project_info_to_disk(self, project_name, info):
		"""
		Writes the info of a project to disk.

		:param project_name: the name of the project.
		:param info: the info to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, project_name)
			self.write_json_to_file(os.path.join(rootfolder, "info.json"), info)

	def write_project_issue_to_disk(self, project_name, issue):
		"""
		Writes an issue of a project to disk.

		:param project_name: the name of the project.
		:param issue: the issue to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, project_name)
			self.write_json_to_file(os.path.join(rootfolder, "issues", str(issue["id"]) + ".json"), issue)
