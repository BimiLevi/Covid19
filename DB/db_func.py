from db.engine import engine

def country_data_toDB(countries_df):
	try:
		countries_list = countries_df['Country'].drop_duplicates().tolist()
		for country in countries_list:
			countryDF = countries_df[countries_df['Country'] == '{}'.format(country)]
			countryDF.to_sql('{}'.format(country), con = engine, if_exists = 'append', index = False)
		print('Countries DB was successfully Updated.')

	except ConnectionError as e:
		print('An error has occurred when trying to update countries DB.')
		raise e

def continent_data_toDB(continent_df):
	try:
		continent_list = continent_df['Continent'].drop_duplicates().tolist()
		for continent in continent_list:
			continentDF = continent_df[continent_df['Continent'] == '{}'.format(continent)]
			continentDF.to_sql('{}'.format(continent), con = engine, if_exists = 'append', index = False)
		print('Continents DB was successfully Updated.')

	except ConnectionError as e:
		print('An error has occurred when trying to update continents DB.')
		raise e

def load_backup_toDB():
	try:
		import time
		start = time.time()

		import pandas as pd
		from paths import mainCountries_path, mainContinents_path
		countries = pd.read_csv(mainCountries_path)
		continents = pd.read_csv(mainContinents_path)

	except FileNotFoundError as e:
		raise e

	try:
		country_data_toDB(countries)
		continent_data_toDB(continents)

		end = time.time()
		execution_time = (end - start) / 60
		print('The process executed successfully,the time it took is: {:.3f} minutes.'.format(execution_time))

	except KeyError as e:
		raise e

def load_backup():
	import os
	from glob import glob
	import pandas as pd
	from paths import world_path

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

		if ext == '*Countries*':
			country_data_toDB(frame)

		elif ext == '*Continents*':
			continent_data_toDB(frame)




if __name__ == '__main__':

	pass