import matplotlib.pyplot as plt
import pandas as pd

from analysis.visualization_func import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 15)

"""Getting the latest data"""
count_update = db.get_table('All countries updated').drop(columns = ['scrap_time'])
conti_update = db.get_table('All continents updated').drop(columns = ['scrap_time'])

top10_activeCases = count_update[['Country', 'ActiveCases']].sort_values('ActiveCases', ascending = False).head(
		10).reset_index(drop=True)

mylist = []
for country in top10_activeCases['Country'].tolist():
		df = db.get_table(country)
		mylist.append(df)

plot = countries_plot('scrap_date', 'ActiveCases', mylist, 'Top countries with active cases', save = True)
plt.show()

