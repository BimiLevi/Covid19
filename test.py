# -*- coding: utf-8 -*-

import time
import timeit
import schedule
import numpy as np
import pandas as pd
import time
from datetime import date, datetime
from tqdm import tqdm

from sqlalchemy import create_engine
from db.config_db import azureParm, localHost

''' This scrip is used to test the program. all of the functions that are required in order for the program to work 
are located in this script. furthermore when testing the program the data is written into localhost DB and not azure! 
'''
def get_data(url):
	from web_driver import Driver
	from bs4 import BeautifulSoup

	counter = 0
	while counter <= 3:
		try:
			bot = Driver()
			bot.driver.get(url)
			content = bot.driver.page_source

			soup = BeautifulSoup(content, 'html5lib')
			table = soup.find('table')

			# Getting the headers for table columns.
			print('Getting the headers.\n')
			table_headers = table.find('tr').findAll('th')
			header_list = []
			for header in table_headers:
				header_list.append(header.get_text())

			# Iterating the data, and creating df.
			records = []
			with tqdm(total = 232, desc = 'Getting the data') as pbar:
				for idy, row in enumerate(table.find_all('tr')):
					time.sleep(0.02)
					pbar.update(1)

					if idy == 0:
						continue
					cols = row.findAll('td')
					record = {}

					for idx, col in enumerate(cols):
						col_text = col.text.strip()
						#
						# if (col_text == 'N/A') or (col_text == ''):  # Filing missing values in the data with numpy nan type.
						# 	record[header_list[idx]] = np.nan
						if col_text == 'N/A':  # Filing missing values in the data with numpy nan type.
							record[header_list[idx]] = (col_text == '')

						else:
							record[header_list[idx]] = col.text.strip()

					records.append(record)

			bot.driver.quit()

			return records

		except IndexError as e:
			print(e, '\n')
			# Three tries before continuing.
			print('The process will start again in 10 seconds.\n This is the {} attempt out of 3.\n'.format(str(
					counter + 1)))
			counter += 1
			time.sleep(10)

	print("The data couldn't be scraped.")

def data_to_dfs(data):
	df = pd.DataFrame.from_dict(data)

	scrap_date = datetime.now().strftime('%d.%m.%y')
	scrap_time = datetime.now().strftime('%H:%M')
	df['scrap_date'] = scrap_date
	df['scrap_time'] = scrap_time

	try:
		drop_cols = ['1 Caseevery X ppl', '1 Deathevery X ppl', '1 Testevery X ppl']
		df = df.drop(columns = drop_cols)

	except FileNotFoundError as e:
		print(e)
		print('The columns you asked for where not found.')


	from process import creat_continentDF, creat_countryDF
	continent_df = creat_continentDF(df)
	country_df = creat_countryDF(df)

	return continent_df, country_df

def add_data_toCsv(countries, continents):
	all_countriesDF = pd.read_csv(r'C:\Users\talle\PycharmProjects\Covid19\all data csvs\all_data_countries.csv')
	all_continentsDF = pd.read_csv(r'C:\Users\talle\PycharmProjects\Covid19\all data csvs\all_data_continents.csv')

	all_countriesDF = pd.concat([all_countriesDF, countries], axis=0, ignore_index=True)
	all_countriesDF.to_csv(r'C:\Users\talle\PycharmProjects\Covid19\all data csvs\all_data_countries.csv', index=False)
	print('Countries entire data csv has been updated.')

	all_continentsDF = pd.concat([all_continentsDF, continents], axis=0, ignore_index=True)
	all_continentsDF.to_csv(r'C:\Users\talle\PycharmProjects\Covid19\all data csvs\all_data_continents.csv', index=False)
	print('Continents entire data csv has been updated.')

def data_toCsvs(countries, continents):
	from process import creat_paths
	dir_paths = creat_paths()

	from utilities.directories import creat_directory
	for path in dir_paths:
		creat_directory(path)

	dateDay_path = dir_paths[3]

	# Saving the data onto a CSV file.
	print('Saving the data to a CSV file.')
	today = date.today()

	files_list = [dateDay_path + '/' + 'Countries {}.csv'.format(str(today)),
	              dateDay_path + '/' + 'Continents {}.csv'.format(str(today))]

	countries.to_csv(files_list[0], index = False)
	print('Countries csv was successfully created.')

	continents.to_csv(files_list[1], index = False)
	print('Continents csv was successfully created.')

dbStr = 'postgresql+psycopg2://{}:{}@{}:{}/{}?client_encoding=utf8"' \
        ''.format(localHost.username, localHost.password, localHost.host, localHost.port, 'covid_test')

engine = create_engine(dbStr, encoding='utf8')

def country_data_toDB(countries_df):
	try:
		countries_list = countries_df['Country'].drop_duplicates().tolist()
		for country in countries_list:
			countryDF = countries_df[countries_df['Country'] == '{}'.format(country)]
			countryDF.to_sql('{}'.format(country), con = engine, if_exists = 'append', index = False)
		print('Countries DB was successfully added.')

	except ConnectionError as e:
		print('An error has occurred when trying to update countries DB.')
		raise e

def continent_data_toDB(continent_df):
	try:
		continent_list = continent_df['Continent'].drop_duplicates().tolist()
		for continent in continent_list:
			continentDF = continent_df[continent_df['Continent'] == '{}'.format(continent)]
			continentDF.to_sql('{}'.format(continent), con = engine, if_exists = 'append', index = False)
		print('Continents DB was successfully added.')

	except ConnectionError as e:
		print('An error has occurred when trying to update continents DB.')
		raise e


if __name__ == '__main__':
	# country_data_toDB(pd.read_csv(r'C:\Users\talle\PycharmProjects\Covid19\old_scripts\all_countries.csv'))
	# df = pd.read_csv(r'C:\Users\talle\PycharmProjects\Covid19\old_scripts\all_continents.csv')
	# continent_data_toDB(df)


	# start = time.time()
	#
	# url = "https://www.worldometers.info/coronavirus"
	# data = get_data(url)
	# continents, countries = data_to_dfs(data)
	# data_toCsvs(countries, continents)
	# continent_data_toDB(continents)
	# country_data_toDB(countries)
	# end = time.time()
	#
	# execution_time = (end - start) / 60
	# print('The process executed successfully,the time it took is: {:.3f} minutes.'.format(execution_time))

	with engine.connect() as connection:
		result = connection.execute("select * from information_schema.tables")
		print(result)
