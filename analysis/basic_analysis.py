import pandas as pd

from analysis.classes import Country, Continent
from database.db_config import current_db as db

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 15)

"""Getting the latest data"""
count_update = db.get_table('All countries updated').drop(columns = ['scrap_time'])
conti_update = db.get_table('All continents updated').drop(columns = ['scrap_time'])


if __name__ == '__main__':
	new_cols = ['NewCases', 'NewRecovered', 'NewDeaths' ]
	active_serious = ['ActiveCases', 'SeriousCritical']
	total_cols = ['TotalCases', 'TotalDeaths', 'TotalRecovered']
	mpop_cols = ['Tot_Cases_1Mpop', 'Deaths_1Mpop', 'Tests_1Mpop']

	country = Country('USA')
	continent = Continent('Europe')

	# country.date_plot(mpop_cols, save = True)
	# country.closed_cases_pie(save = True)
	# country.monthly_plot(new_cols, 10, 2020, save = True)

	# continent.monthly_plot(['NewCases', 'NewRecovered', 'NewDeaths'], 10, 2020, save = False)
	# continent.closed_cases_pie(save = False)
	# continent.date_plot(new_cols, save = False)

	# plt.show()



