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
local_user = os.environ.get('username_local')
local_pass = os.environ.get('dbPass_local')
local_dbName = os.environ.get('dbName_local')
local_host = os.environ.get('host_local')

localHost = Db(local_user, local_pass, local_dbName, local_host)

# Localhost db - TEST!
test_dbName = os.environ.get('dbName_test')

localTest = Db(local_user, local_pass, test_dbName, local_host)

# Azure
azure_user = os.environ.get('username_azure')
azure_pass = os.environ.get('dbPass_azure')
azure_dbName = os.environ.get('dbName_azure')
azure_host = os.environ.get('host_azure')

azureParm = Db(azure_user, azure_pass, azure_dbName, azure_host)
