from paths import countriesID_path, continentsID_path
country_path = countriesID_path
continent_path = continentsID_path

from utilities.files_function import load_json
possible_continents = load_json(continent_path)
possible_countries = load_json(country_path)


def creat_continentDF(df):
	try:
		continents_list = possible_continents.keys()
		continent_df = df[df['Country,Other'].isin(continents_list)]
		continent_df = continent_df.drop(columns = ['#', 'TotalTests', 'Population', 'Continent', 'Deaths/1M pop'],
		                                 axis = 1)

		continent_df = continent_df.rename(columns = {'Country,Other': 'Continent'})

		# Giving each continent a uniq id parm.
		continent_df['Continent_id'] = continent_df['Continent'].map(possible_continents)


		col_list = ['scrap_date', 'scrap_time', 'Continent_id', 'Continent', 'TotalCases', 'NewCases',
		            'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious,Critical']

		continent_df = continent_df.reindex(columns = col_list)

		return continent_df

	except KeyError as e:
		raise e

def creat_countryDF(df):
	try:
		country_first_idx = df[df['#'] == str(1)].index.tolist()[0]  # Getting the starting index' in order
		# To slice the df.
		country_df = df[country_first_idx:]
		country_df = country_df[country_df['Country,Other'] != 'Total:'].reset_index(drop = True)

		# Giving each country an uniq id parm.
		country_df['#'] = country_df['Country,Other'].map(possible_countries)
		country_df['Continent'] = country_df['Continent'].map(possible_continents)
		country_df = country_df.rename(columns = {'Country,Other': 'Country', '#': 'Country_id',
		                                          'Continent': 'Continent_id',
		                                          'Tests/\n1M pop\n': 'Tests_1M_pop',
		                                         'Tot\xa0Cases/1M pop': 'Tot_Cases_1M_pop'})


		col_list = ['scrap_date', 'scrap_time', 'Country_id', 'Country', 'Population', 'TotalCases', 'NewCases',
		            'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious,Critical',
		            'Tot_Cases_1M_pop', 'Deaths/1M pop', 'TotalTests', 'Tests_1M_pop', 'Continent_id']

		df = df.reindex(columns = col_list)
		country_df = country_df.reindex(columns = col_list)
		country_df

		return country_df

	except KeyError as e:
		raise e

def get_date_parm():
	from datetime import datetime
	year = datetime.now().strftime("%Y")
	month = datetime.now().strftime("%B")
	day = datetime.now().strftime("%d")
	return day, month, year

