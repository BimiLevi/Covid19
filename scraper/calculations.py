import numpy as np
import pandas as pd

from database.db_config import current_db as db


def get_last_row(tableName):
	row = db.get_table(tableName).tail(1)
	return row

def calc_new_cases(df):
	series = None
	try:
		dif = df['TotalCases'].diff()
		df['NewCases'] = dif
		series = df['NewCases'].iloc[1]

	except Exception as e:
		print(e)

	finally:
		return series

def calc_new_deaths(df):
	series = None
	try:
		dif = df['TotalDeaths'].diff()
		df['NewDeaths'] = dif
		series = df['NewDeaths'].iloc[1]

	except Exception as e:
		print(e)

	finally:
		return series

def calc_new_recovered(df):
	series = None
	try:
		dif = df['TotalRecovered'].diff()
		df['NewRecovered'] = dif
		series = df['NewRecovered'].iloc[1]

	except Exception as e:
		print(e)

	finally:
		return series

def make_calc(df, tableName):
	try:
		pd.options.mode.chained_assignment = None  # default='warn'

		last_row = get_last_row(tableName)

		tempdf = pd.concat([last_row, df]).reset_index(drop=True)

		for col in ['TotalCases','NewCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered']:
			tempdf[col] = tempdf[col].astype('float64')

		df['NewCases'] = calc_new_cases(tempdf)
		df['NewDeaths'] = calc_new_deaths(tempdf)
		df['NewRecovered'] = calc_new_recovered(tempdf)


	except Exception as e:
		df['NewCases'] = np.nan
		df['NewDeaths'] = np.nan
		df['NewRecovered'] = np.nan

	finally:

		return df
