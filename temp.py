import pandas as pd

from database.db_config import current_db as db

pd.options.mode.chained_assignment = None  # default='warn'


if __name__ == '__main__':
	israel = db.get_table('Israel')





