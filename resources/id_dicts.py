import pandas as pd

from scraper.scraper import run_scraper, data_to_dfs
from utilities.files_function import *

"""
This script creates a uniq id for each county / continent, based on the scraped data.
"""

def continents_to_json(continent_df):
	continents_list = continent_df['Continent'].to_list()
	continents_table = {}

	for idx, continent in enumerate(continents_list, start = 1):
		continents_table[continent] = idx

	save_json(continents_table, 'Continents table ')

def countries_to_json(countries_df):
	countries_list = countries_df['Country'].to_list()
	countries_ids = {}

	for idx, country in enumerate(countries_list, start = 1):
		countries_ids[country] = idx

	save_json(countries_ids, 'Countries id')

	countriesDict = countries_ids.fromkeys(countries_ids)
	countries_table = pd.Series(countriesDict).reset_index()
	countries_table = countries_table.drop([0], axis = 1)
	countries_table = countries_table.rename(columns = {'index': 'Country'})
	countries_table['Country_id'] = countries_table['Country'].map(countries_ids)

	countries_df = countries_df[['Country_id', 'Continent_id']]
	countries_table = countries_table.merge(countries_df, on = 'Country_id')

	save_json(countries_table, 'Countries table')

def creat_base_tables():

	data = run_scraper()
	continents, countries = data_to_dfs(data)

	continents_to_json(continents)

	countries_to_json(countries)


