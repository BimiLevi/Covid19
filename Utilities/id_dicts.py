from world_meter_scraper import get_data, data_to_dfs
from utilities.files_function import *

"""
This script creates a uniq id for each county / continent, based on the scraped data.
Therefore this script should only be executed once - The first time scraping the data. 
"""

if __name__ == '__main__':
	countries_keys = load_json('countries id')
	continents_keys = load_json('continent id')

	url = "https://www.worldometers.info/coronavirus"

	data = get_data(url)

	continents, countries = data_to_dfs(data)

	continents_list = continents['Continent'].to_list()
	continents_dict = {}

	countries_list = countries['Country'].to_list()
	countries_dict = {}

	for idx, continent in enumerate(continents_list, start = 1):
		continents_dict[continent] = idx

	for idx, country in enumerate(countries_list, start = 1):
		countries_dict[country] = idx


	json_save(continents_dict, 'continent id')
	json_save(countries_dict, 'countries id')

