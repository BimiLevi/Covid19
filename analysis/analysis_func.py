import pandas as pd

from database.db_config import current_db

db = current_db
countries = pd.read_sql('All Countries', con = db.get_engine())
continents = pd.read_sql('All Continents', con = db.get_engine())
countries_continents = countries.merge(continents, on = 'Continent_id')

def country_parm(countryName):
	df = countries_continents[countries_continents['Country'] == countryName]
	continent_id = df['Continent_id'].unique()[0]
	country_id = df['Country_id'].unique()[0]
	country = df['Country'].unique()[0]
	parm = {'continent_id': continent_id, 'country_id': country_id, 'country': country}
	return parm

def data_by_month(df, month):
	if type(month) != int:
		raise TypeError('Month must be of int type.')

	data = df[df['scrap_date'].dt.month == month]
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

def get_top(df, col, n=10):

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
		sorted_df = df[['Country', col]]	.sort_values(col, ascending = False)
		top = sorted_df.head(n).reset_index(drop = True)
		return top

	else:
		return 'Error neither countries or continents were called.'

def get_table_list(names):
	df_list = []

	for name in names:
		df = db.get_table(name)
		df_list.append(df)

	return df_list



