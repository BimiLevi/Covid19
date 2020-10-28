import pandas as pd

from database.tables_parm import *
from resources.paths import countries_path, continents_path


def continents_table(engine):
	try:
		continents = pd.read_json(continents_path + '.json', orient = 'index').reset_index()
		continents = continents.rename(columns = {'index': 'Continent', 0: 'Continent_id'})
		continents = continents.reindex(columns = ['Continent_id', 'Continent'])
		continents.to_sql('All Continents', con = engine, index = False, dtype=continents_parm)
		print('Continents table has been successfully created.\n')

	except Exception as e:
		print('The following Exception as occurred:\n{}'.format(e))

def countries_table(engine):
	try:
		countries = pd.read_json(countries_path + '.json', orient = 'columns')
		countries.to_sql('All Countries', con = engine, index = False, dtype=countries_parm)
		print('Countries table has been successfully created.\n')

	except Exception as e:
		print('The following Exception as occurred:\n{}'.format(e))
