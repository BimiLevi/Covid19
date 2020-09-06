import numpy as np
import pandas as pd
import time
from datetime import date, datetime
from progressbar import progressbar
from tqdm import tqdm


def get_data(url):
	from web_driver import Driver
	from bs4 import BeautifulSoup

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
	counter = 0
	while counter != 3:
		try:
			with tqdm(total = 232, desc= 'Getting the data') as pbar:
				for idy, row in enumerate(table.find_all('tr')):
					time.sleep(0.02)
					pbar.update(1)

					if idy == 0:
						continue
					cols = row.findAll('td')
					record = {}

					for idx, col in enumerate(cols):
						col_text = col.text.strip()

						if (col_text == 'N/A') or (col_text == ''): # Filing missing values in the data with numpy nan type.
							record[header_list[idx]] = np.nan

						else:
							record[header_list[idx]] = col.text.strip()

					records.append(record)

			bot.driver.quit()

			return records

		except IndexError as e:
			print(e)
			# Three tries before continuing.
			counter += 1
			time.sleep(3)

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
		print('The columns you asked for where not found.')
		print(e)

	from process import creat_continentDF, creat_countryDF
	continent_df = creat_continentDF(df)
	country_df = creat_countryDF(df)

	return continent_df, country_df

def data_toCsvs(countries, continents):
	from process import creat_paths
	dir_paths = creat_paths()
	from Utilities.directories import creat_directory
	for path in dir_paths:
		creat_directory(path)

	dateDay_path = dir_paths[3]

	# Saving the data onto a CSV file.
	print('Saving the data to a CSV file.')
	today = date.today()

	files_list = [dateDay_path + '/' + 'Countries {}.csv'.format(str(today)),
	              dateDay_path + '/' + 'Continents {}.csv'.format(str(today))]

	countries.to_csv(files_list[0], index=False)
	print('Countries csv was successfully created.')

	continents.to_csv(files_list[1], index=False)
	print('Continents csv was successfully created.')

if __name__ == '__main__':
	from DB.db_func import *
	start = time.time()

	url = "https://www.worldometers.info/coronavirus"
	data = get_data(url)
	continents, countries = data_to_dfs(data)
	data_toCsvs(countries, continents)
	continent_data_toDB(continents), country_data_toDB(countries)
	end = time.time()

	execution_time = (end - start)
	print('The process executed successfully,the time it took is: {:.3f} seconds.'.format(execution_time))




