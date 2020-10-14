import time
from datetime import datetime

import requests as req
from bs4 import BeautifulSoup
from tqdm import tqdm

from resources.paths import continents_path, countries_id, site_url
from utilities.files_function import load_json


def get_html(url = site_url):
	try:
		print('Getting html page.')
		html_page = req.get(url)
		print('Html page retrieved.\n')

		return html_page

	except req.exceptions.RequestException as e:
		print('Unable to get html page.')
		print("The error that occurred is:\n{}\n".format(e))

def get_table(html_page):
	print('Finding the table with the data.')
	soup = BeautifulSoup(html_page.content, 'html5lib')
	table = soup.find('table')
	print('Table found.\n')
	return table

def process_table(table):
	print('Starting to processes the table.')
	def get_headers_list(table_headers):
		header_list = []
		for header in table_headers:
			header_list.append(header.get_text())
		return header_list

	headers_list = get_headers_list(table.find('tr').findAll('th'))
	rows = table.findAll('tr')

	# Iterating the data, and creating df.
	records = []
	total_data = 0
	with tqdm(total = len(rows), desc = 'Processing the data') as pbar:
		for idy, row in enumerate(rows):
			time.sleep(0.02)
			pbar.update(1)

			cols = row.findAll('td')
			record = {}

			for idx, col in enumerate(cols):
				col_text = col.text.strip()
				if (col_text == 'N/A') or (col_text == ''):  # Filing missing values in the data with None
					record[headers_list[idx]] = None

				else:
					if ',' in col_text:
						col_text = col_text.replace(',', '')

					if '+' in col_text:
						col_text = col_text.replace('+', '')
					record[headers_list[idx]] = col_text

			total_data += 1
			records.append(record)

	print('The data was extracted from the table.\n')
	return records

def creat_continent_df(df):
	try:
		possible_continents = load_json(continents_path)

	except Exception as e:
		print("Unable to load continents json file.")
		print("The error that occurred is:\n{}".format(e))

	try:
		continents_list = possible_continents.keys()
		continent_df = df[df['Country,Other'].isin(continents_list)]

	except KeyError as e:
		raise e

	except Exception as e:
		print("Unable to retrieve the continents from the data.")
		print("The error that occurred is:\n{}".format(e))

	try:
		continent_df = continent_df.drop(columns = ['#', 'TotalTests', 'Population', 'Continent', 'Deaths/1M pop'],
		                                 axis = 1)
	except Exception as e:
		print("Couldn't drop the requested columns from the df.")
		print("The error that occurred is:\n{}".format(e))

	try:
		continent_df = continent_df.rename(columns = {'Country,Other': 'Continent'})
		# Giving each continent a uniq id parm.
		continent_df['Continent_id'] = continent_df['Continent'].map(possible_continents)

	except KeyError as e:
		print("The error that occurred is:\n{}".format(e))

	except Exception as e:
		print("Unable to map continents ID's / rename DF columns.")
		print("The error that occurred is:\n{}".format(e))

	try:
		col_list = ['scrap_date', 'scrap_time', 'Continent_id', 'Continent', 'TotalCases', 'NewCases',
		            'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious,Critical']

		continent_df = continent_df.reindex(columns = col_list)

	except Exception as e:
		print("Couldn't rename columns names.")
		print("The error that occurred is:\n{}".format(e))

	return continent_df

def creat_country_df(df):
	try:
		countryId_dict = load_json(countries_id)

	except Exception as e:
		print("Unable to load countries id json file.")
		print("The error that occurred is:\n{}".format(e))

	try:
		country_df = df[df[df['#'] == str(1)].index.tolist()[0]:]
		country_df = country_df[country_df['Country,Other'] != 'Total:'].reset_index(drop = True)

	except Exception as e:
		print("Unable to manipulate tha data indexes ")
		print("The error that occurred is:\n{}".format(e))

	try:
		# Giving each country an uniq id parm.
		country_df['#'] = country_df['Country,Other'].map(countryId_dict)

		import pandas as pd
		from resources.paths import countries_path
		countriesTable = pd.read_json(countries_path + '.json')
		country_df['Continent'] = country_df['Country,Other'].map(countriesTable.set_index('Country')['Continent_id'])


	except Exception as e:
		print("Couldn't map tha data, during processing stage.")
		print("The error that occurred is:\n{}".format(e))

	try:
		country_df = country_df.rename(columns = {'Country,Other': 'Country', '#': 'Country_id',
		                                          'Continent': 'Continent_id',
		                                          'Tests/\n1M pop\n': 'Tests_1M_pop',
		                                         'Tot\xa0Cases/1M pop': 'Tot_Cases_1M_pop'})


		col_list = ['scrap_date', 'scrap_time', 'Country_id', 'Country', 'Population', 'TotalCases', 'NewCases',
		            'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious,Critical',
		            'Tot_Cases_1M_pop', 'Deaths/1M pop', 'TotalTests', 'Tests_1M_pop', 'Continent_id']

		country_df = country_df.reindex(columns = col_list)

	except Exception as e:
		print("Couldn't rename / reorder DF columns.")
		print("The error that occurred is:\n{}".format(e))

	return country_df

def get_date_parm():
	year = datetime.now().strftime("%Y")
	month = datetime.now().strftime("%B")
	day = datetime.now().strftime("%d")
	return day, month, year

