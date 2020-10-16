from datetime import date

import pandas as pd

from process_func import *
from resources.paths import creat_paths
from utilities.directories import creat_directory


def run_scraper():
	start = time.time()
	counter = 1
	while counter <= 3:
		try:
			html = get_html()
			soup = html_parser(html)
			update_date, update_time = latest_update(soup)
			table = get_table(soup)
			data = process_table(table)
			break

		except IndexError as ie:
			counter += 1
			print('Unable to process the data due to IndexError.')
			print("The error that occurred is:\n{}\n".format(ie))

			# Three tries before continuing.
			print('The process will start again in 30 seconds.\n This is the {} attempt out of 3.\n'.format(str(
					counter)))
			time.sleep(30)

	end = time.time()
	execution_time = (end - start) / 60
	print('The process executed successfully.\nthe time it took to scrape the data is: {:.3f} minutes.'.format(
			execution_time))
	return data, update_date, update_time

def data_to_dfs(data, update_date, update_time):
	df = pd.DataFrame.from_dict(data)

	scrap_date = datetime.now().strftime('%Y-%m-%d')
	scrap_time = datetime.now().strftime('%H:%M')
	df['scrap_date'] = scrap_date
	df['scrap_time'] = scrap_time

	df['update date'] = update_date
	df['update time-GMT'] = update_time

	try:
		drop_cols = ['1 Caseevery X ppl', '1 Deathevery X ppl', '1 Testevery X ppl']
		df = df.drop(columns = drop_cols)

	except FileNotFoundError as e:
		print('The columns you asked for where not found.'
		      'The requested columns are:\n{]'.format(drop_cols))
		print("The error that occurred is:\n{}".format(e))


	continent_df = creat_continent_df(df)
	country_df = creat_country_df(df)

	return continent_df, country_df

def data_to_csvs(countries, continents):
	dir_paths = creat_paths()

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


