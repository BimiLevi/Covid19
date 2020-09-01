class Db:
	def __init__(self, username, password, dbname, host, port = 5432 ):
		self.username = username
		self.password = password
		self.dbname = dbname
		self.host = host
		self.port = port

# Localhost DB
localHost = Db('username1', 'password1', 'dbname1', 'localhost')

# Azure
azureParm = Db('username2', 'password2', 'dbname2', 'host')



