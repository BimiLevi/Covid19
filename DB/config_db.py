class Db:
    def __init__(self, username, password, dbname, host, port=5432):
        self.username = username
        self.password = password
        self.dbname = dbname
        self.host = host
        self.port = port

    def __str__(self):
        return'''
username: {}
password: {}
db name: {}
host/server: {}
port: {}'''.format(self.username, self.password, self.dbname, self.host, self.port)

import os

# Localhost DB

localHost_parm = {
    'host': os.environ.get('host_local'),
    'database': os.environ.get('dbName_local'),
    'user': os.environ.get('username_local'),
    'password': os.environ.get('dbPass_local')
    }

localHost = Db(localHost_parm['user'], localHost_parm['password'], localHost_parm["database"], localHost_parm['host'])

# Localhost db - TEST!
localTest_parm = {
    'host': os.environ.get('host_local'),
    'database': os.environ.get('dbName_test'),
    'user': os.environ.get('username_local'),
    'password': os.environ.get('dbPass_local')
    }

localTest = Db(localTest_parm['user'], localTest_parm["password"], localTest_parm['database'], localTest_parm['host'])

# Azure
azureHost_parm = {
    'host': os.environ.get('host_azure'),
    'database': os.environ.get('dbName_azure'),
    'user': os.environ.get('username_azure'),
    'password': os.environ.get('dbPass_azure')
    }

azure = Db(azureHost_parm['user'], azureHost_parm['password'], azureHost_parm['database'], azureHost_parm['host'])


