from scraper.world_meter_scraper import get_data, data_to_dfs
from utilities.files_function import *
import pandas as pd

"""
This script creates a uniq id for each county / continent, based on the scraped data.
"""

def continents_to_json(continent_df):
	continents_list = continent_df['Continent'].to_list()
	continents_table = {}

	for idx, continent in enumerate(continents_list, start = 1):
		continents_table[continent] = idx

	json_save(continents_table, 'Continents table ')

def countries_to_json(countries_df):
	countries_list = countries_df['Country'].to_list()
	countries_ids = {}

	for idx, country in enumerate(countries_list, start = 1):
		countries_ids[country] = idx

	json_save(countries_ids, 'Countries id')

	countriesDict = countries_ids.fromkeys(countries_ids)
	countries_table = pd.Series(countriesDict).reset_index()
	countries_table = countries_table.drop([0], axis = 1)
	countries_table = countries_table.rename(columns = {'index': 'Country'})
	countries_table['Country_id'] = countries_table['Country'].map(countries_ids)

	countries_df = countries_df[['Country_id', 'Continent_id']]
	countries_table = countries_table.merge(countries_df, on = 'Country_id')

	json_save(countries_table, 'Countries table')

def creat_base_tables():
	from resources.paths import site_url

	url = site_url

	data = get_data(url)

	continents, countries = data_to_dfs(data)

	continents_to_json(continents)

	countries_to_json(countries)


