import pandas as pd

from database.db_config import current_db

db = current_db

def country_parm(df):
	continent_id = df['Continent_id'].unique()[0]
	country_id = df['Country_id'].unique()[0]
	country = df['Country'].unique()[0]
	population = df['Population'].unique()[0]
	parm = {'continent_id': continent_id, 'country_id': country_id, 'country': country, 'Population': population}
	return parm

def get_minmax(df, col):
	min_val = df[df[col] == df[col].min()][col]
	max_val = df[df[col] == df[col].max()][col]
	min_max = pd.concat([min_val, max_val]).reset_index()
	return min_max

countries = pd.read_sql('All Countries', con = db.get_engine())
continents = pd.read_sql('All Continents', con = db.get_engine())
countries_continents = countries.merge(continents, on = 'Continent_id')
print(countries_continents)

israel = pd.read_sql('Israel', con = db.get_engine())
print(israel.columns.tolist)