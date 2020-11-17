from database.db_config import current_db as db

data = db.get_table('All countries updated')
df = data
