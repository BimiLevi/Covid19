from resources.paths import countries_path, continents_path
from db.engine import engine
import pandas as pd


def continents_table():
	try:
		continents = pd.read_json(continents_path + '.json', orient = 'index').reset_index()
		continents = continents.rename(columns = {'index': 'Continent', 0: 'Continent_id'})
		continents = continents.reindex(columns = ['Continent_id', 'Continent'])
		continents.to_sql('Continents', con = engine, index = False)
		print('Continents table has been successfully created.\n')

	except Exception as e:
		print('The following Exception as occurred:\n{}'.format(e))

def countries_table():
	try:
		countries = pd.read_json(countries_path + '.json', orient = 'columns')
		countries.to_sql('Countries', con = engine, index = False)
		print('Countries table has been successfully created.\n')

	except Exception as e:
		print('The following Exception as occurred:\n{}'.format(e))
