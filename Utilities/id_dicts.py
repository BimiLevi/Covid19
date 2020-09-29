from scraper.world_meter_scraper import get_data, data_to_dfs
from utilities.files_function import *
import pandas as pd

# TODO: Maybe there is n need for this script.
"""
This script creates a uniq id for each county / continent, based on the scraped data.
Therefore this script should only be executed once - The first time scraping the data. 
"""

if __name__ == '__main__':
	from resources.paths import site_url
	url = site_url

	data = get_data(url)

	continents, countries = data_to_dfs(data)

	continents_list = continents['Continent'].to_list()
	continents_table = {}

	for idx, continent in enumerate(continents_list, start = 1):
		continents_table[continent] = idx

	countries_list = countries['Country'].to_list()
	countries_ids = {}

	for idx, country in enumerate(countries_list, start = 1):
		countries_ids[country] = idx

	countriesDict = countries_ids.fromkeys(countries_ids)
	countries_table = pd.Series(countriesDict).reset_index()
	countries_table = countries_table.drop([0], axis=1)
	countries_table = countries_table.rename(columns= {'index': 'Country'})
	countries_table['Country_id'] = countries_table['Country'].map(countries_ids)

	countries = countries[['Country_id', 'Continent_id']]
	countries_table = countries_table.merge(countries, on='Country_id')

	json_save(continents_ids, 'Continents table ')
	json_save(countries_table, 'Countries table')
	json_save(countries_ids, 'Countries id')
