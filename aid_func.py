"""Iterating all the csv files in directory """
def iterate_csv():
	import os
	from glob import glob
	from resources.paths import world_path
	import pandas as pd
	try:
		# Complexity time O(n^3)
		ext_list = ["*Countries*", '*Continents*']
		for ext in ext_list:
			for path, subdir, files in os.walk(world_path):
				for csv_path in glob(os.path.join(path, ext)):
					df = pd.read_csv(csv_path, index_col = None, header = 0)

					if ext == "*Countries*":
						col_list = ['scrap_date', 'scrap_time', 'update date', 'update time-GMT', 'Country_id',
						            'Country','Population', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
						            'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious,Critical',
						            'Tot_Cases_1M_pop', 'Deaths/1M pop', 'TotalTests', 'Tests_1M_pop', 'Continent_id']

						df = df.reindex(columns = col_list)

					elif ext == '*Continents*':
						col_list = ['scrap_date', 'scrap_time', 'update date', 'update time-GMT', 'Continent_id',
						            'Continent',
						            'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered',
						            'NewRecovered', 'ActiveCases', 'Serious,Critical']

						df = df.reindex(columns = col_list)

					df['update date'] = df['scrap_date']
					df.to_csv(csv_path, index = False)



	except Exception as e:
		print('The following Exception as occurred:\n{}'.format(e))

iterate_csv()