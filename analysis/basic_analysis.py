import matplotlib.pyplot as plt
import pandas as pd

from database.db_config import current_db
from resources.paths import plots_path

plt.style.use('classic')
plt.rcParams['font.sans-serif'] = 'SimSun'
plt.rcParams['savefig.dpi'] = 600
plt.rcParams["figure.dpi"] = 100
plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False})
color_palette = {'black': '#3D3D3D', 'blue': '#3F5E99', 'yellow': '#EBCA88', 'red': '#F04A6B', 'green': '#3AB08B'}

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

def get_minmax(df, col):
	min_val = df[df[col] == df[col].min()][col]
	max_val = df[df[col] == df[col].max()][col]
	min_max = pd.concat([min_val, max_val]).reset_index(drop=True)
	return min_max

def data_by_month(df, month):
	if type(month) != int:
		raise TypeError('Month must be of int type.')
	
	data = df[df['scrap_date'].dt.month == month]
	return data.reset_index(drop=True)

def data_range_date(df, startDate, endDate):
	firstDate = df['scrap_date'].min().date()
	lastDate = df['scrap_date'].max().date()

	startDate = pd.to_datetime(startDate).date()
	endDate = pd.to_datetime(endDate).date()

	if (startDate < firstDate) or (endDate > lastDate) or (startDate > endDate):
		raise ValueError('One of the dates surpass boundaries')

	data = df[(str(startDate) <= df['scrap_date']) & (df['scrap_date'] <= str(endDate))].reset_index(drop=True)
	return data

def color_minmax(df, col):
    colors = []
    min_val = df[col].min()
    max_val = df[col].max()
    for val in df[col]:
        if val == max_val:
            colors.append(color_palette['green'])
        elif val == min_val:
            colors.append(color_palette['red'])
        else:
            colors.append(color_palette['blue'])
    return colors

israel = pd.read_sql('Israel', con = db.get_engine())

def bar_plot(df, col, month = None, startDate = None, endDate = None, save = False):

	if month is not None:
		data = data_by_month(df, month)
		data = data[['scrap_date', col]]



	elif (startDate is not None) and (endDate is not None):
		data = data_range_date(df, startDate, endDate)

	else:
		"""return the the avg of each month since the start """
		return -1

	data = data[data[col].notna()]
	x = data['scrap_date'].dt.day
	y = data[col]

	fig = plt.figure(figsize=(19.20, 10.80), edgecolor = 'b')
	colors = color_minmax(df, col)

	plot = plt.bar(x, y, color=colors, align='center', width = 0.5, figure = fig)

	plt.tick_params(right = False, top = False)
	plt.xticks(range(len(x.index)), x.values.tolist())
	plt.xlim(left = x.min()-1, right = x.max()+1)

	plt.xlabel('Date', figure = fig)
	plt.ylabel(col, figure = fig)
	plt.title('temp', figure = fig)


	if save:
		file_format = 'svg'
		fname = 'temp.{}'.format(file_format)
		plt.savefig(plots_path + r'\{}'.format(fname), format=file_format, edgecolor='b',bbox_inches='tight')


	return plot



# bar_plot(israel, 'NewCases', startDate = '2020-08-02', endDate= '2020-09-21', save = True)
bar_plot(israel, 'NewCases', month = 10, save = True)
plt.show()

