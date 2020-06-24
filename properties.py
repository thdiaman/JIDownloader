# Set this to your Jira installation API URL
JiraAPI = "https://add.here.the.URL.of.your.jira/rest/api/2/"

# Set this to your Jira username and password
JiraCredentials = ('add_here_your_username', 'add_here_your_password')

# Set this to False to skip existing projects
update_existing_projects = True

# Set to 0 for no messages, 1 for simple messages, and 2 for progress bars
verbose = 1

# Select how to write to disk (or how to send queries to the database)
always_write_to_disk = True

# Change these settings to store data in disk/database
use_database = 'disk' # (available options: disk, mongo)
# Disk settings
dataFolderPath = 'data' # Set this to the folder where data are downloaded
# Database settings
database_host_and_port = "mongodb://localhost:27017/"  # change this to the hostname and port of your database
num_bulk_operations = 1000 # set the number of operations that are sent as a bulk to the database

# Select which issue fields to download (set to "all", "custom", "jira", or to specific fields, e.g. "summary,description,status")
issue_fields = "jira"

# Select which issue fields to expand (set to "none" or to specific fields, e.g. "changelog,renderedFields")
issue_expands = "changelog"
