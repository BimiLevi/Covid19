
'''Before lunching the program for the first time, dont forget to check that paths below are correct.'''

from paths import countriesID_path, continentsID_path
country_path = countriesID_path
continent_path = continentsID_path

from utilities.files_function import load_json
possible_continents = load_json(continent_path)
possible_countries = load_json(country_path)

'''
    OR: Python functions should be lower cased. "create_continent_df(df)"
'''
def creat_continentDF(df):
    '''
    OR: try-except too long
    '''
	try:
		continents_list = possible_continents.keys()
		continent_df = df[df['Country,Other'].isin(continents_list)]
		continent_df = continent_df.drop(columns = ['#', 'TotalTests', 'Population', 'Continent', 'Deaths/1M pop'],
		                                 axis = 1)

		continent_df = continent_df.rename(columns = {'Country,Other': 'Continent'})

		# Giving each continent a uniq id parm.
		continent_df['Continent_id'] = continent_df['Continent'].map(possible_continents)

		column_titles = ['Continent_id', 'Continent', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
		                 'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious,Critical', 'scrap_date',
		                 'scrap_time']

		continent_df = continent_df.reindex(columns = column_titles)

		return continent_df

	except KeyError as e:
		raise e

def creat_countryDF(df):
	try:
		'''
		OR: Too many operations in 1 function. maybe sub-functions? split the responsability
		'''
		country_first_idx = df[df['#'] == str(1)].index.tolist()[0]  # Getting the starting index' in order
		# To slice the df.
		country_df = df[country_first_idx:]
		country_df = country_df[country_df['Country,Other'] != 'Total:'].reset_index(drop = True)

		# Giving each country an uniq id parm.
		country_df['#'] = country_df['Country,Other'].map(possible_countries)
		country_df['Continent'] = country_df['Continent'].map(possible_continents)
		country_df = country_df.rename(columns = {'Country,Other': 'Country', '#': 'Country_id',
		                                          'Continent': 'Continent_id',
		                                          'Tests/\n1M pop\n': 'Tests_1M_pop'})

		desired_cols = country_df.iloc[:, 2:].drop(columns= ['Population']).columns.tolist()
		col_titles = ['Country_id', 'Country', 'Population'] + desired_cols
		country_df = country_df.reindex(columns = col_titles)

		return country_df

	except KeyError as e:
		raise e

def get_date_parm():
    '''
    OR: Why not use extrenal import? (from the top of the script)
    '''
	from datetime import datetime
	year = datetime.now().strftime("%Y")
	month = datetime.now().strftime("%B")
	day = datetime.now().strftime("%d")
	return day, month, year

def creat_paths():
	day, month, year = get_date_parm()

	# Crating directories to save the scraped data in them.
	from utilities.directories import path
	#  Crating path for each directory.
	world_path = path + '/' + "World Meter Data"
	dateYea_path = world_path + '/' + year
	dateMon_path = dateYea_path + '/' + month
	dateDay_path = dateMon_path + '/' + day

	dir_paths = [world_path, dateYea_path, dateMon_path, dateDay_path]

	return dir_paths
