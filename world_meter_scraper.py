import numpy as np
import pandas as pd
import time
from datetime import date, datetime
from tqdm import tqdm


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
			print('Getting the headers.')
			table_headers = table.find('tr').findAll('th')
			header_list = []
			for header in table_headers:
				header_list.append(header.get_text())

			# Iterating the data, and creating df.
			records = []
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

						if (col_text == 'N/A') or (col_text == ''):  # Filing missing values in the data with numpy nan type.
							record[header_list[idx]] = np.nan

						else:
							record[header_list[idx]] = col.text.strip()

					records.append(record)

			bot.driver.quit()

			return records

		except IndexError as e:
			bot.driver.quit()
			print(e, '\n')
			# Three tries before continuing.
			print('The process will start again in 10 seconds.\n This is the {} attempt out of 3.\n'.format(str(
					counter+1)))
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
		print('The columns you asked for where not found.')
		print(e)

	from process import creat_continentDF, creat_countryDF
	continent_df = creat_continentDF(df)
	country_df = creat_countryDF(df)

	return continent_df, country_df

def data_toCsvs(countries, continents):
	import process
	dir_paths = process.creat_paths()

	from utilities.directories import creat_directory
	for path in dir_paths:
		creat_directory(path)

	dateDay_path = dir_paths[3]

	# Saving the data onto a CSV file.
	print('Saving the data to a CSV file.')
	today = date.today()

	files_list = [dateDay_path + '/' + 'Countries {}.csv'.format(str(today)),
	              dateDay_path + '/' + 'Continents {}.csv'.format(str(today))]

	countries.to_csv(files_list[0], index=False)
	print('Countries {} csv was successfully created.'.format(str(today)))

	continents.to_csv(files_list[1], index=False)
	print('Continents {} csv was successfully created.'.format(str(today)))

def update_main_csvs(countries, continents):
	try:
		from paths import allContinents_path, allCountries_path

		try:
			all_countriesDF = pd.read_csv(allCountries_path)
			if not countries.empty:
				all_countriesDF = pd.concat([all_countriesDF, countries], axis = 0, ignore_index = True)
				all_countriesDF.to_csv(allCountries_path, index = False)
				print('Countries main data csv has been updated.')

		except OSError as e:
			print("The main csv's did not updated the following Error has occurred: \n {}".format(e))
			print('Countries main file, dose not exists.')
			countries.to_csv(allCountries_path, index=False)
			print('Countries main csv has been created.')

		try:
			all_continentsDF = pd.read_csv(allContinents_path)
			if not countries.empty:
				all_continentsDF = pd.concat([all_continentsDF, continents], axis=0, ignore_index=True)
				all_continentsDF.to_csv(allContinents_path, index=False)
				print('Continents main csv has been updated.')

		except OSError as e:
			print("The main csv's did not updated the following Error has occurred: \n {}".format(e))
			continents.to_csv(allContinents_path, index = False)
			print('Continents main csv has been created.')

	except Exception as e:
		print("The main csv's did not updated the following Error has occurred: \n {}".format(e))
		print("There is no main csv's files.")


