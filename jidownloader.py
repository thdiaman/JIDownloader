import os
import sys
import traceback
from logger.downloadlogger import Logger
from datamanager.dbmanager import DBManager
from datamanager.mongomanager import MongoDBManager
from downloader.jiradownloader import JiraDownloader
from helpers import get_number_of, print_usage, read_file_in_lines
from properties import JiraAPI, JiraCredentials, update_existing_projects, verbose, issue_fields, issue_expands, use_database

# Initialize all required objects
db = MongoDBManager() if use_database == 'mongo' else DBManager()
lg = Logger(verbose)
jd = JiraDownloader(JiraAPI, JiraCredentials)

def download_project(project_name):
	"""
	Downloads all the data of a project given its Jira name.

	:param project_name: the name of the projects of which the data are downloaded.
	"""
	project_api_address = JiraAPI + "project/" + project_name

	lg.log_action("Downloading project " + project_name)
	if db.project_exists(project_name):
		if update_existing_projects:
			lg.log_action("Project already exists! Updating...")
		else:
			lg.log_action("Project already exists! Skipping...")
			return

	db.initialize_write_to_disk(project_name)

	project = db.read_project_from_disk(project_name)

	try:
		project_info = jd.download_object(project_api_address)
		project.add_info(project_info)
		db.write_project_info_to_disk(project_name, project["info"])

		project_issues_address = JiraAPI + "search"
		number_of_issues = get_number_of(jd, project_issues_address, "jql=project=" + project_name)

		# Create params
		issue_params = ["jql=project=" + project_name]
		if issue_fields == "jira" or issue_fields == "custom":
			fields = jd.download_object(JiraAPI + "field")
			fields = [field for field in fields if field["custom"] == (issue_fields == "custom")]
			issue_params.append("fields=" + ",".join(f["id"] for f in fields))
		elif issue_fields != "all":
			issue_params.append("fields=" + issue_fields)
		issue_params.append("expand=" + issue_expands)

		lg.start_action("Retrieving issues...", number_of_issues)
		for issue in jd.download_paginated_object(project_issues_address, "issues", issue_params):
			project.add_issue(issue)
			db.write_project_issue_to_disk(project_name, issue)
			lg.step_action()
		lg.end_action()

	except Exception:
		# Catch any exception and print it before exiting
		sys.exit(traceback.format_exc())
	finally:
		# This line of code is always executed even if an exception occurs
		db.finalize_write_to_disk(project_name, project)

if __name__ == "__main__":
	if ((not sys.argv) or len(sys.argv) <= 1):
		print_usage()
	elif(os.path.exists(sys.argv[1])):
		projects = read_file_in_lines(sys.argv[1])
		for project in projects:
			download_project(project)
	elif(len(sys.argv[1]) > 0):
		download_project(sys.argv[1])
	else:
		print_usage()

