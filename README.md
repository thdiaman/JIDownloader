JIDownloader: Jira Issue Downloader
===================================
JIDownloader is a data downloader for the Jira API. The tool allows to download project information
and all issues of Jira projects. The tool uses the Jira API v2, for which more
information can be found [here](https://developer.atlassian.com/cloud/jira/platform/rest/v2/).

Prerequisites
-------------
The python library requirements are available in file `requirements.txt` and may be installed using
the command `pip install -r requirements.txt`.

To run this tool, you must have a Jira installation and an account. You must set these details in file `properties.py`.

Executing the tool
------------------
To run the tool, one must first correctly assign the properties in file `properties.py`.
After that, the tool can be executed by running `python jidownloader.py [jira_project_name_or_list_of_names]`,
where `jira_project_name_or_list_of_names` must be replaced by either one of the following:
- a Jira project name (e.g. `MyJiraProject`)
- a list of Jira project names, as a text file where each file is a Jira project name
If a project already exists in the data folder, then its data are updated.

The main parameters are the following:
- `JiraAPI`: the API URL of the Jira installation (if Jira is installed at `https://issues.myorganization.org/jira/` then the URL should be `https://issues.myorganization.org/jira/rest/api/2/`)
- `JiraCredentials`: the username and the password of your Jira account (provided as a tuple, e.g. `('myusername', 'mypassword')`)
- `update_existing_projects`: controls whether the existing (already downloaded) projects will be updated or skipped
- `verbose`: controls the messages in the standard output (0 for no messages, 1 for simple messages, and 2 for progress bars)
- `always_write_to_disk`: controls whether the project data will be written on download (always) or after fully downloading them

Controlling where data are saved
--------------------------------
The data can be stored either in disk or in a database. Currently, the tool supports two options: disk storage and
MongoDB. These options are controlled using the `use_database` parameter and are outlined below.

To use the disk, the `use_database` parameter must be set to `"disk"`. Disk storage includes the following options:
- `dataFolderPath`: the path where the data will be downloaded (without trailing slash/backslash)

To store the data in a database, one has to download and set up [MongoDB](https://www.mongodb.com/) and then set the
parameter `use_database` to `"mongo"`. Database storage includes the following options:
- `database_host_and_port`: the hostname and port of the database to store the data into
- `num_bulk_operations`: controls the number of operations that are sent as a bulk to the database (optimization parameter)

Controlling what is downloaded
------------------------------
One can also control which issue data are downloaded by setting the following variables:
- `issue_fields`: controls which issue fields are downloaded, can be set to `"all"` for all fields, to `"custom"` for the custom fields, to `"jira"` for the default jira fields, or to specific fields as a comma-separated (no spaces) list, e.g. `"summary,description,status"`
- `issue_expands`: controls which issue fields are expanded, can be set to `"none"` or to specific fields as a comma-separated (no spaces) list, e.g. `"changelog,renderedFields"`
