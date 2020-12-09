import pandas as pd



def get_data():
	df = None
	try:
		df = pd.read_csv(r'C:\playtika\presentation\Marketing Academy Test  Data.csv')
		print('The data was successfully loaded')

	except Exception as e:
		print(f'Unable to load the data\n{e}')

	finally:
		return df
