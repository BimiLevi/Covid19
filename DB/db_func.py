from db.engine import engine
from resources.tables_func import *
import pandas as pd
import psycopg2

def load_backup():
	import time
	import os
	from glob import glob
	from resources.paths import world_path
	try:
		start = time.time()

		print('Creating Countries main table')
		countries_table()

		print('Creating Continents main table')
		continents_table()

		# Complexity time O(n^3)
		ext_list = ["*Countries*", '*Continents*']
		for ext in ext_list:
			all_csv_files = []
			for path, subdir, files in os.walk(world_path):
				for csv_path in glob(os.path.join(path, ext)):
					df = pd.read_csv(csv_path, index_col = None, header = 0)
					all_csv_files.append(df)

			frame = pd.concat(all_csv_files, axis = 0, ignore_index = True)
			frame = frame.sort_values('scrap_date')

			if ext == "*Countries*":
				df_to_db('Country', frame)

			elif ext == '*Continents*':
				df_to_db('Continent', frame)

		end = time.time()
		execution_time = (end - start) / 60
		print('The process executed successfully,the time it took is: {:.3f} minutes.\n'.format(execution_time))

	except Exception as e:
		print('The following Exception as occurred:\n{}'.format(e))

def get_tables_names():
	tables_list = []
	with engine.connect() as con:
		res = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
		tables = res.fetchall()
		for table in tables:
			tables_list.append(table[0])

	return tables_list

def table_exists(table):
	tables_list = get_tables_names()

	if table in tables_list:
		return True

	else:
		return False

def df_to_db(col, df):
	try:
		from db.tables_parm import countries_parm, continents_parm
		parm = None
		if col == 'Country':
			parm = countries_parm

		elif col == 'Continent':
			parm = continents_parm

		headers_list = df[col].drop_duplicates().tolist()
		for header in headers_list:
			temp_df = df[df[col] == '{}'.format(header)]
			temp_df.to_sql('{}'.format(header), con = engine, if_exists = 'append', index = False)

		print('{} DB was successfully Updated.'.format(col))

	except ConnectionError as e:
		print('Unable to connect to DB.')
		raise e

	except Exception as e:
		print("Couldn't dump the data in to DB.")
		print("The error that occurred is:\n{}".format(e))
# This func returns pandas object.
def get_table(table):
	try:
		if type(table) == str:
			if not table[0].isupper():
				table = table.capitalize()

			if table_exists(table):
				table = pd.read_sql(table, con = engine)
				return table

			else:
				return "The table that you requested doesn't exists in the DB."

		else:
			return 'The input must be of str type.'

	except psycopg2.Error as e:
		print("The error that occurred is:\n{}".format(e))
		raise ValueError("Unable to connect to DB.")



