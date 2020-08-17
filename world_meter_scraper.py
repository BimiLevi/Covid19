import numpy as np
import pandas as pd
from datetime import date, datetime


def get_data(url):
	from web_driver import Driver
	from bs4 import BeautifulSoup

	bot = Driver()
	bot.driver.get(url)
	content = bot.driver.page_source

	soup = BeautifulSoup(content, 'html5lib')
	table = soup.find('table')

	# Getting the headers for table columns.
	print('Getting the headers.')
	table_headers = table.find('tr').findAll('th')
	header_list = []
	for header in table_headers:
		header_list.append(header.get_text())

	# Iterating the data, and creating df.
	print('Getting the data.\n')
	records = []

	try:
		for idy, row in enumerate(table.find_all('tr')):
			if idy == 0:
				continue
			cols = row.findAll('td')
			record = {}
			for idx, col in enumerate(cols):
				col_text = col.text.strip()
				if (col_text == 'N/A') or (col_text == ''):  # Filing missing values in the data with numpy nan object.
					record[header_list[idx]] = np.nan
				else:
					record[header_list[idx]] = col.text.strip()
			records.append(record)

		entire_data = pd.DataFrame.from_dict(records)

		bot.driver.quit()
		return entire_data

	except IndexError as e:
		print(e)

def creat_subDF(df):
	# Splitting the entire dataset into parts by continents, and countries.

	# Continents.
	continents_list = ['North America', 'South America', 'Asia', 'Europe', 'Africa', 'Oceania', 'World']
	continent_df = df[df['Country,Other'].isin(continents_list)]
	continent_df = continent_df.drop(continent_df.iloc[:, 13:continent_df.shape[1]], axis = 1)
	continent_df = continent_df.drop(columns = ['#', 'TotalTests'], axis = 1)
	continent_df = continent_df.rename(columns = {'Country,Other': 'Continent'})

	# Countries.
	country_first_idx = df[df['#'] == str(1)].index.tolist()[0]  # Getting the starting index' in order
	# To slice the df.
	country_df = df[country_first_idx:]
	country_df = country_df[country_df['Country,Other'] != 'Total:'].reset_index(drop = True)
	country_df = country_df.drop(columns = ['#', '1 Caseevery X ppl', '1 Deathevery X ppl', '1 Testevery X ppl'])
	country_df = country_df.rename(columns = {'Country,Other': 'Country'})

	return continent_df, country_df

def get_date_parm():
	year = datetime.now().strftime("%Y")
	month = datetime.now().strftime("%B")
	day = datetime.now().strftime("%d")
	return day, month, year

def creat_paths():
	day, month, year = get_date_parm()

	# Crating directories to dave the scraped data.
	from Utilities.directories import path
	#  Crating path for each directory.
	world_path = path + '/' + "World Meter Data"
	dateYea_path = world_path + '/' + year
	dateMon_path = dateYea_path + '/' + month
	dateDay_path = dateMon_path + '/' + day

	dir_paths = [world_path, dateYea_path, dateMon_path, dateDay_path]

	return dir_paths

def data_toCsv(countries, continents):
	from Utilities.directories import creat_directory
	dir_paths = creat_paths()

	for path in dir_paths:
		creat_directory(path)

	dateDay_path = dir_paths[3]

	# Saving the data onto a CSV file.
	print('Saving the data to a CSV file.\n')
	today = date.today()

	files_list = [dateDay_path + '/' + 'Countries {}.csv'.format(str(today)),
	              dateDay_path + '/' + 'Continents {}.csv'.format(str(today))]

	countries.to_csv(files_list[0])
	print('Countries Csv was successfully created')
	continents.to_csv(files_list[1])
	print('Continents Csv was successfully created')

if __name__ == '__main__':
	url = "https://www.worldometers.info/coronavirus"

	data = get_data(url)

	continents, countries = creat_subDF(data)

	data_toCsv(countries, continents)
