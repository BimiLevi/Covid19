class Db:
	def __init__(self, username, password, dbname, host, port = 5432):
		self.username = username
		self.password = password
		self.dbname = dbname
		self.host = host
		self.port = port

# Localhost DB
localHost = Db('username1', 'DBpassword1', 'DBname1', 'localhost')

# Azure
azureParm = Db('username2', 'DBpassword2', 'DBname2', 'azurehost2')



