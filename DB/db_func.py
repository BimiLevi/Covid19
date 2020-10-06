from db.engine import engine
import sqlalchemy as sa
import  pandas as pd

def load_backup():
	import time
	import os
	from glob import glob
	import pandas as pd
	from resources.paths import world_path
	try:
		start = time.time()

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

def get_all_tables():
	tables_list = []
	with engine.connect() as con:
		res = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
		tables = res.fetchall()
		for table in tables:
			tables_list.append(table[0])

	return tables_list

def table_exists(table):
	tables_list = get_all_tables()

	if table in tables_list:
		return True

	else:
		return False

def df_to_db(col, df):
	try:
		headers_list = df[col].drop_duplicates().tolist()
		for header in headers_list:
			temp_df = df[df[col] == '{}'.format(header)]
			temp_df.to_sql('{}'.format(header), con = engine, if_exists = 'append', index = False)

		print('{} DB was successfully Updated.'.format(col))

	except ConnectionError as e:
		print('Unable to connect to DB.')
		raise e

	except Exception as e:
		print("Couldn't dump tha data in to DB.")
		print("The error that occurred is:\n{}".format(e))

def get_country(countryName):
	if not countryName[0].isupper():
		countryName = countryName.capitalize()

	country = sa.Table(countryName, sa.MetaData(), autoload_with = engine)
	query = country.select()
	result = engine.execute(query).fetchall()
	print(result)
	return result

	# with engine.connect() as con:
	# 	res = con.execute("SELECT * FROM information_schema.tables WHERE table_schema='public'")
	# 	tables = res.fetchall()
	# 	for table in tables:
	# 		pass

		# return 1




# israel = get_country('israel')
temp = pd.read_sql('Israel',con = engine)
print(type(israel))
# print(israel)
print(temp)