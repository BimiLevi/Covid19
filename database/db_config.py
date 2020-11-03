import os

from database.db import Db

localHost_parm = {
	'host': os.environ.get('host_local'),
	'database': os.environ.get('dbName_local'),
	'user': os.environ.get('username_local'),
	'password': os.environ.get('dbPass_local')
	}

# Localhost db - TEST!
localTest_parm = {
	'host': os.environ.get('host_local'),
	'database': os.environ.get('dbName_test'),
	'user': os.environ.get('username_local'),
	'password': os.environ.get('dbPass_local')
	}

# Azure
azureHost_parm = {
	'host': os.environ.get('host_azure'),
	'database': os.environ.get('dbName_azure'),
	'user': os.environ.get('username_azure'),
	'password': os.environ.get('dbPass_azure')
	}

localHost = Db(localHost_parm['user'], localHost_parm['password'], localHost_parm["database"],
               localHost_parm['host'])

localTest = Db(localHost_parm['user'], localHost_parm['password'], localTest_parm["database"],
               localHost_parm['host'])

azure = Db(azureHost_parm['user'], azureHost_parm['password'], azureHost_parm['database'], azureHost_parm['host'])

current_db = localHost




