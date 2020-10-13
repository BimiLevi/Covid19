import pandas as pd
import time
from datetime import date, datetime
from tqdm import tqdm

def get_data(url):
	global bot
	from scraper.web_driver import Driver
	from bs4 import BeautifulSoup

	counter = 1
	while counter <= 3:
		try:
			bot = Driver()
			bot.driver.get(url)
			content = bot.driver.page_source

			soup = BeautifulSoup(content, 'html5lib')
			table = soup.find('table')

			# Getting the headers for table columns.
			print('Getting the headers.')
			table_len = len(table.findAll('tr'))
			table_headers = table.find('tr').findAll('th')

			header_list = []
			for header in table_headers:
				header_list.append(header.get_text())

			# Iterating the data, and creating df.
			records = []
			total_data = 1
			with tqdm(total = table_len, desc= 'Getting the data') as pbar:
				for idy, row in enumerate(table.find_all('tr')):
					time.sleep(0.02)
					pbar.update(1)

					if idy == 0:
						continue
					cols = row.findAll('td')
					record = {}

					for idx, col in enumerate(cols):
						col_text = col.text.strip()
						if (col_text == 'N/A') or (col_text == ''):  # Filing missing values in the data with None
							record[header_list[idx]] = None

						else:
							if ',' in col_text:
								col_text = col_text.replace(',', '')

							if '+' in col_text:
								col_text = col_text.replace('+', '')
							record[header_list[idx]] = col_text

					total_data += 1
					records.append(record)

			bot.driver.quit()

			if total_data != table_len:
				raise ValueError('The data was not scraped completely.\n ')


			return records

		except Exception as e:
			bot.driver.quit()
			print("The error that occurred is:\n{}\n".format(e))
			# Three tries before continuing.
			print('The process will start again in 10 seconds.\n This is the {} attempt out of 3.\n'.format(str(
					counter+1)))
			counter += 1
			time.sleep(10)

	print("The data couldn't be scraped.")

def data_to_dfs(data):
	df = pd.DataFrame.from_dict(data)

	scrap_date = datetime.now().strftime('%Y-%m-%d')
	scrap_time = datetime.now().strftime('%H:%M')
	df['scrap_date'] = scrap_date
	df['scrap_time'] = scrap_time

	try:
		drop_cols = ['1 Caseevery X ppl', '1 Deathevery X ppl', '1 Testevery X ppl']
		df = df.drop(columns = drop_cols)

	except FileNotFoundError as e:
		print('The columns you asked for where not found.'
		      'The requested columns are:\n{]'.format(drop_cols))
		print("The error that occurred is:\n{}".format(e))


	from scraper.process_func import creat_continent_df, creat_country_df
	continent_df = creat_continent_df(df)
	country_df = creat_country_df(df)

	return continent_df, country_df

def data_to_csvs(countries, continents):
	from resources.paths import creat_paths
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

	countries.to_csv(files_list[0], index=False)
	print('Countries {} csv was successfully created.'.format(str(today)))

	continents.to_csv(files_list[1], index=False)
	print('Continents {} csv was successfully created.'.format(str(today)))