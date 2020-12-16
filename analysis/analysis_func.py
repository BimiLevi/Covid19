import calendar

import numpy as np
import pandas as pd
import pycountry as pc
from geopy.geocoders import Nominatim

from utilities.files_function import load_json

geolocator = Nominatim(user_agent = "https")

from resources.paths import countriesCodes_path

def data_by_month(df, month, year):
	if type(month) != int:
		raise TypeError('Month must be of int type.')

	data = df[(df['scrap_date'].dt.month == month) & (df['scrap_date'].dt.year == year)]
	return data.reset_index(drop = True)

def data_range_date(df, startDate, endDate):
	firstDate = df['scrap_date'].min().date()
	lastDate = df['scrap_date'].max().date()

	startDate = pd.to_datetime(startDate).date()
	endDate = pd.to_datetime(endDate).date()

	if (startDate < firstDate) or (endDate > lastDate) or (startDate > endDate):
		raise ValueError('One of the dates surpass boundaries')

	data = df[(str(startDate) <= df['scrap_date']) & (df['scrap_date'] <= str(endDate))].reset_index(drop = True)
	return data

def get_minmax(df, col):
	min_val = df[df[col] == df[col].min()][col]
	max_val = df[df[col] == df[col].max()][col]

	min_max = pd.concat([min_val, max_val])
	return min_max

def get_top(df, col, n = 10):
	if (type(n) != int) or (type(col) != str):
		raise TypeError('n = int, col = str')

	elif not isinstance(df, pd.DataFrame):
		raise TypeError('df = dataframe')

	col_list = df.columns.tolist()

	if 'Continent' in col_list:
		if col == 'TotalTests':
			return

		sorted_df = df[['Continent', col]].sort_values(col, ascending = False)
		top = sorted_df.head(n).reset_index(drop = True)
		return top

	elif 'Country' in col_list:
		sorted_df = df[['Country', col]].sort_values(col, ascending = False)
		top = sorted_df.head(n).reset_index(drop = True)
		return top

	else:
		return 'Error neither countries or continents were called.'

def first_day_of_month(date):
	day = calendar.weekday(date.year, date.month, 1)
	return calendar.day_name[day]

def geolocate(country):
	loc = None

	try:
		loc = geolocator.geocode(country)
		loc = (loc.latitude, loc.longitude)

	except:
		loc = np.nan

	finally:
		return loc

def countries_codes(df):
	countries = {}
	for country in pc.countries:
		countries[country.name] = country.alpha_3

	codes = []
	for country in df['Country']:

		if country in countries.keys():
			codes.append(countries.get(country))

		elif country in countries.values():
			codes.append(country)

		else:
			try:
				check_res = pc.countries.search_fuzzy(country)[0].alpha_3
				codes.append(check_res)

			except LookupError:
				codes.append('Null')

	return codes

def get_alpha_3(country):
	countries = load_json(countriesCodes_path)

	if country in countries.keys():
		code = countries.get(country)

	elif country in countries.values():
		code = country

	else:
		try:
			check_res = pc.countries.search_fuzzy(country)[0].alpha_3
			code = check_res

		except LookupError:
			code = np.nan

	return code

# def report(territory_name):


