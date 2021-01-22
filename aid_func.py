import os
from glob import glob

import pandas as pd

from database.db_config import current_db as db
from resources.paths import Ddate_path

sample_dict = {'scrap_date': '2020-10-28', 'scrap_time': '10:00', 'update_time_GMT': None, 'Country_id': [1],
     'Country': 'tal', 'Population': [1], 'TotalCases': [1000000], 'NewCases': [5000],
     'TotalDeaths': [1000000], 'NewDeaths': [5000], 'TotalRecovered': [1000000], 'NewRecovered': [5000],
     'ActiveCases': [0], 'SeriousCritical': [0], 'Tot_Cases_1Mpop': [0], 'Deaths_1Mpop': [0], 'TotalTests': [0],
     'Tests_1Mpop': [0]}

def iterate_countries_csv():
	for path, subdir, files in os.walk(Ddate_path):
		for csv_path in glob(os.path.join(path, "*Countries*")):
			df = pd.read_csv(csv_path, index_col = None, header = 0)
			''' add the relevant action here~'''
			df['Scrap_time'] = df['Date'] + ' ' + df['Scrap_time']
			col_list = ['Scrap_time', 'Update_time_GMT', 'Date', 'Country_id', 'Country', \
			            'Population', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered',
			            'NewRecovered', 'ActiveCases', 'SeriousCritical',
			            'Tot_Cases_1Mpop', 'Deaths_1Mpop', 'TotalTests', 'Tests_1Mpop']
			
			df = df.reindex(columns=col_list)
			# df.to_csv(r'C:\Users\talle\PycharmProjects\Covid19\test\ ' + os.path.basename(csv_path), index= False)
			df.to_csv(csv_path, index = False)

def iterate_continents_csv():
	for path, subdir, files in os.walk(Ddate_path):
		for csv_path in glob(os.path.join(path, '*Continents*')):
			df = pd.read_csv(csv_path, index_col = None, header = 0)
			''' add the relevant action here~'''
			df['Scrap_time'] = df['Date'] + ' ' + df['Scrap_time']
			col_list = ['Scrap_time', 'Update_time_GMT', 'Date', 'Continent_id', 'Continent',
			            'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered',
			            'NewRecovered', 'ActiveCases', 'SeriousCritical']

			df = df.reindex(columns = col_list)
			# df.to_csv(r'C:\Users\talle\PycharmProjects\Covid19\test\ ' + os.path.basename(csv_path), index = False)
			df.to_csv(csv_path, index = False)

def get_last_row(tableName):
	row = db.get_table(tableName).tail(1)
	return row

def calc_new_cases(df):
	series = None
	try:
		dif = df['TotalCases'].diff()
		df['NewCases'] = dif
		series = df['NewCases']

	except Exception as e:
		print(e)

	finally:
		return series

def calc_new_deaths(df):
	series = None
	try:
		dif = df['TotalDeaths'].diff()
		df['NewDeaths'] = dif
		series = df['NewDeaths']

	except Exception as e:
		print(e)

	finally:
		return series

def calc_new_recovered(df):
	series = None
	try:
		dif = df['TotalRecovered'].diff()
		df['NewRecovered'] = dif
		series = df['NewRecovered']

	except Exception as e:
		print(e)

	finally:
		return series

def calculations(df, tableName):
	try:
		pd.options.mode.chained_assignment = None  # default='warn'

		last_row = get_last_row(tableName)

		tempdf = pd.concat([last_row, df]).reset_index(drop=True)

		df['NewCases'] = calc_new_cases(tempdf)
		df['NewDeaths'] = calc_new_deaths(tempdf)
		df['NewRecovered'] = calc_new_recovered(tempdf)

		return df

	except Exception as e:
		print(e)

if __name__ == '__main__':
	pass

	iterate_countries_csv()
	iterate_continents_csv()

	# israel = db.get_table('Israel')

	# print(israel[['NewCases', 'NewDeaths', 'NewRecovered']].head(10))
	# print(israel[['TotalCases', 'TotalDeaths', 'TotalRecovered']].head(10))
	#
	# print('---------------------------------------------------------------------------------------------------------')
	# df = israel
	# df['NewCases'] = calc_new_cases(df)
	# df['NewDeaths'] = calc_new_deaths(df)
	# df['NewRecovered'] = calc_new_recovered(df)
	# print(df[['NewCases', 'NewDeaths', 'NewRecovered']].head(10))

