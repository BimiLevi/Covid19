from DB.engine import engine

def country_data_toDB(countries_df):
	try:
		countries_list = countries_df['Country'].drop_duplicates().tolist()
		for country in countries_list:
			countryDF = countries_df[countries_df['Country'] == '{}'.format(country)]
			countryDF.to_sql('{}'.format(country), con = engine, if_exists = 'append', index = False)
		print('Countries DB was successfully added.')

	except ConnectionError as e:
		print('An error has occurred when trying to update countries DB.')
		raise e

def continent_data_toDB(continent_df):
	try:
		continent_list = continent_df['Continent'].drop_duplicates().tolist()
		for continent in continent_list:
			continentDF = continent_df[continent_df['Continent'] == '{}'.format(continent)]
			continentDF.to_sql('{}'.format(continent), con = engine, if_exists = 'append', index = False)
		print('Continents DB was successfully added.')

	except ConnectionError as e:
		print('An error has occurred when trying to update continents DB.')
		raise e
