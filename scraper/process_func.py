from resources.paths import continents_path, countries_id
from utilities.files_function import load_json
from datetime import datetime

possible_continents = load_json(continents_path)
countryId_dict = load_json(countries_id)

def creat_continent_df(df):
	try:
		continents_list = possible_continents.keys()
		continent_df = df[df['Country,Other'].isin(continents_list)]

	except KeyError as e:
		raise e

	except Exception as e:
		print("Unable to retrieve the continents from the data.")
		print("The error that occurred is:\n{}".format(e))

	try:
		continent_df = continent_df.drop(columns = ['#', 'TotalTests', 'Population', 'Continent', 'Deaths/1M pop'],
		                                 axis = 1)
	except Exception as e:
		print("Couldn't drop the requested columns from the df.")
		print("The error that occurred is:\n{}".format(e))

	try:
		continent_df = continent_df.rename(columns = {'Country,Other': 'Continent'})
		# Giving each continent a uniq id parm.
		continent_df['Continent_id'] = continent_df['Continent'].map(possible_continents)

	except KeyError as e:
		print("The error that occurred is:\n{}".format(e))

	except Exception as e:
		print("Unable to map continents ID's / rename DF columns.")
		print("The error that occurred is:\n{}".format(e))

	try:
		col_list = ['scrap_date', 'scrap_time', 'Continent_id', 'Continent', 'TotalCases', 'NewCases',
		            'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious,Critical']

		continent_df = continent_df.reindex(columns = col_list)

	except Exception as e:
		print("Couldn't rename columns names.")
		print("The error that occurred is:\n{}".format(e))

	return continent_df

def creat_country_df(df):
	try:
		country_df = df[df[df['#'] == str(1)].index.tolist()[0]:]
		country_df = country_df[country_df['Country,Other'] != 'Total:'].reset_index(drop = True)

	except Exception as e:
		print("Unable to manipulate tha data indexes ")
		print("The error that occurred is:\n{}".format(e))

	try:
		# Giving each country an uniq id parm.
		country_df['#'] = country_df['Country,Other'].map(countryId_dict)
		country_df['Continent'] = country_df['Continent'].map(possible_continents)

	except Exception as e:
		print("Couldn't map tha data, during processing stage.")
		print("The error that occurred is:\n{}".format(e))

	try:
		country_df = country_df.rename(columns = {'Country,Other': 'Country', '#': 'Country_id',
		                                          'Continent': 'Continent_id',
		                                          'Tests/\n1M pop\n': 'Tests_1M_pop',
		                                         'Tot\xa0Cases/1M pop': 'Tot_Cases_1M_pop'})


		col_list = ['scrap_date', 'scrap_time', 'Country_id', 'Country', 'Population', 'TotalCases', 'NewCases',
		            'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious,Critical',
		            'Tot_Cases_1M_pop', 'Deaths/1M pop', 'TotalTests', 'Tests_1M_pop', 'Continent_id']

		country_df = country_df.reindex(columns = col_list)

	except Exception as e:
		print("Couldn't rename / reorder DF columns.")
		print("The error that occurred is:\n{}".format(e))

	return country_df

def get_date_parm():
	year = datetime.now().strftime("%Y")
	month = datetime.now().strftime("%B")
	day = datetime.now().strftime("%d")
	return day, month, year

