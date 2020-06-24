import json

def get_number_of(jdownloader, project_api_address, parameter = None):
	"""
	Posts a request using an instance of JiraDownloader and returns the number of
	a given statistic (e.g. number of issues, number of commits, etc.).

	:param jdownloader: an instance of JiraDownloader.
	:param project_api_address: the address from where the statistic is downloaded.
	:param parameter: an optional parameter for the statistic.
	:returns: the value for the statistic as an absolute number.
	"""
	r = jdownloader.download_request(project_api_address, ["maxResults=1"] if parameter == None else ["maxResults=1", parameter])
	data = json.loads(r.text or r.content) if r.status_code != 204 else {}
	return data["total"]

def read_file_in_lines(filename):
	"""
	Reads a file into lines.

	:param filename: the filename of the file to be read.
	:returns: a list with the lines of the file.
	"""
	with open(filename) as infile:
		lines = infile.readlines()
	return [line.strip() for line in lines]

def print_usage():
	"""
	Prints the usage information of this python file.
	"""
	print("Usage: python jidownloader.py arg")
	print("where arg can be one of the following:")
	print("   project name (e.g. MyProject)")
	print("   path to txt file containing project names")

