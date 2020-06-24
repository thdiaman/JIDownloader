
class Project(dict):
	"""
	Class that includes the data of a Jira project. This class is implemented as a dict
	and includes also several helper functions for adding data and checking for data.
	"""
	def info_exists(self):
		"""
		Checks if the info of the project exists.

		:returns: True if the project info exists, or False otherwise.
		"""
		return bool(self["info"])

	def add_info(self, info):
		"""
		Adds the info of the project.

		:param info: the info to be added to the project.
		"""
		self["info"] = info

	def issue_exists(self, issue):
		"""
		Checks if the given issue exists in the project.

		:param issue: the issue to be checked.
		:returns: True if the given issue exists in the project, or False otherwise.
		"""
		return issue["id"] in self["issues"]

	def add_issue(self, issue):
		"""
		Adds an issue to the project.

		:param issue: the issue to be added to the project.
		"""
		self["issues"][issue["id"]] = issue
