class Db:
	def __init__(self, username, password, dbname, host, port = 5432 ):
		self.username = username
		self.password = password
		self.dbname = dbname
		self.host = host
		self.port = port

# Localhost DB
localHost = Db('postgres', 'A123465789', 'COVID19', 'localhost')

# Azure
azureParm = Db('TalLevi@postgresql12', 'Bimidb6285!', 'Covid19', 'postgresql12.postgres.database.azure.com')



