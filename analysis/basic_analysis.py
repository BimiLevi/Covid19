from analysis.analysis_func import *
from analysis.visualization_func import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 15)

"""Getting the latest data"""
count_update = db.get_table('All countries updated').drop(columns = ['scrap_time'])
conti_update = db.get_table('All continents updated').drop(columns = ['scrap_time'])

cols = ['TotalCases', 'TotalDeaths', 'TotalRecovered', 'ActiveCases', 'SeriousCritical', 'TotalTests']

if __name__ == '__main__':

	"""
	Top ten countries by different criteria.
	"""

	for col in cols:
		top = get_top(count_update, col)
		count_list = top['Country'].to_list()

		df_list = get_table_list(count_list)
		date_plot(col, df_list, save = False, title = 'Top ten countries {}'.format(col))

	"""
	Top  continents by different criteria.
	"""

	for col in cols:
		top = get_top(conti_update, col)
		count_list = top['Continent'].to_list()

		df_list = get_table_list(count_list)
		date_plot(col, df_list, save = False, title = 'Top continents {}'.format(col))

	plt.show()
