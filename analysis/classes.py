import re
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from analysis.analysis_func import *
from analysis.visualization_func import *
from database.db_config import current_db as db
from resources.paths import *
from utilities.files_function import load_json

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 15)

class Territory:
	def __init__(self, name, ttype):
		self.name = name.lower()
		self.ttype = ttype.lower()

class Country(Territory):
	numeric_cols = ['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'ActiveCases',
	                 'SeriousCritical', 'Tot_Cases_1Mpop', 'Deaths_1Mpop', 'TotalTests', 'Tests_1Mpop']

	def __init__(self, name, ttype):
		super().__init__(name, ttype)

		self.data = db.get_table(self.name)

		self.id = self.data['Country_id'].unique()[0]

		temp = pd.DataFrame(load_json(countries_path))
		self.continent_id = int(temp[temp['Country_id'] == self.id]['Continent_id'].unique()[0])

		temp = load_json(continents_path)
		temp = dict([(value, key) for key, value in temp.items()])
		self.continent = temp[self.continent_id]

		self.population = self.data['Population'][0]
		self.last_update = self.data['scrap_date'].max().date()
		self.first_update = self.data['scrap_date'].min().date()

		self.data = self.data.drop(columns =['Population', 'update_time_GMT', 'Country_id', 'Country'])

		self.size = self.data.shape
		self.columns = self.data.columns.tolist()

	def __str__(self):
		return """
Countries name: {}
Countries id: {}
Continent: {}
Continent id: {}
Population: {}
First update: {}
Last update: {}
Data number of rows: {}
Data number of columns: {}
Columns: \n{}
		""".format(self.name.capitalize(), self.id, self.continent, self.continent_id, self.population,
		           self.first_update, self.last_update, self.size[0], self.size[1], self.columns)


	def refresh(self):
		if (type(self.name) is str) and (self.name is not None) :
			self.data = db.get_table(self.name)

	def get_data(self):
		return self.data

	def date_plot(self, cols = numeric_cols, start_date = None, end_date = None, save = False):
		if type(cols) != list:
			raise TypeError('Type must be a list.')

		if len(cols) == 0:
			raise ValueError('cols list is empty.')

		if (start_date is not None) and (end_date is not None):
			data = data_range_date(self.data, start_date, end_date)

		else:
			data = self.data

		fig = plt.figure(figsize = (19.20, 10.80), tight_layout = True)
		ax = fig.add_subplot()


		for i, col in enumerate(cols):
			values = data[col]
			col_title = " ".join(re.findall('[A-Z][^A-Z]*', col))


			ax.plot(data['scrap_date'], values, linewidth=3, label = col_title, color=color_palette[i])

			handles, labels = ax.get_legend_handles_labels()
			if '_' in col_title:
				new_title = col.replace('_', ' ', -1)
				for idx, label in enumerate(labels):
					if label == col_title:
						labels[idx] = new_title

			ax.legend(handles, labels, bbox_to_anchor = (1.001, 1), loc = "best", frameon = True, edgecolor = 'black',
				          fontsize = 20)

		ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday = 6, interval = 1))
		ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))

		ax.xaxis.grid(True, which = "minor")
		ax.yaxis.grid()
		ax.xaxis.set_major_locator(mdates.MonthLocator())
		ax.xaxis.set_major_formatter(mdates.DateFormatter('\n\n\n%b\n%Y'))

		xtitle = 'Date'
		ytitle = 'Values'

		ax.set_xlabel(xtitle, fontsize = 15, fontweight = 'bold')
		ax.set_ylabel(ytitle, fontsize = 15, fontweight = 'bold')
		ax.set_title('{}'.format(self.name.capitalize()), fontsize = 17, fontweight = 'bold')

		if save:
			title = input('Please enter plots name\n')
			file_format = 'svg'
			fig.savefig('{}\{}.{}'.format(plots_path, title, file_format), format = file_format, edgecolor = 'b',
			bbox_inches ='tight')

		return ax

	def closed_cases_pie(self, save = False):
		fig, ax = plt.subplots(figsize = (19.20, 10.80), tight_layout = True)

		cases = self.data[self.data['scrap_date'] == self.data['scrap_date'].max()]
		cases = cases[['TotalCases', 'ActiveCases', 'TotalRecovered', 'TotalDeaths']]

		nclosed = (cases['TotalCases'] - cases['ActiveCases']).tolist()[0]

		ratio = cases[['TotalRecovered', 'TotalDeaths']] / nclosed
		idx = ratio.index

		t_ratio = ratio.T.rename(columns={idx[0]: 'x'})

		explode = np.ones(t_ratio.shape[0]) * 0.05
		labels = ratio.columns.tolist()
		colors = ['yellowgreen', 'lightcoral']

		pie = ax.pie(t_ratio['x'], labels = labels, shadow = True, startangle = 90, explode =
		explode, pctdistance = 0.85, colors=colors,normalize=True,textprops={'fontsize': 20})

		legend_labels = round(t_ratio['x'] * 100, 3).astype(str) + '%'

		ax.legend(pie[0], legend_labels, loc = "center left", bbox_to_anchor = (1, 0, 0.5, 1),prop={'size': 20})

		centre_circle = plt.Circle((0, 0), 0.70, fc = 'white')
		fig = plt.gcf()
		fig.gca().add_artist(centre_circle)

		ax.set_title('{} Closed Cases Ratio'.format(self.name.capitalize()), fontsize = 25, fontweight = 'bold')

		if save:
			title = '{} Closed Cases Ratio'.format(self.name.capitalize())
			file_format = 'svg'
			fig.savefig('{}\{}.{}'.format(plots_path, title, file_format), format = file_format, edgecolor = 'b',
			bbox_inches ='tight')



		return pie

	def monthly_bar(self, cols, month, year, save = False):
		if len(cols) > 4:
			raise ValueError('The maximum amount of columns is 4.')


		if month is not None:
			data = data_by_month(self.data, month,year)

		else:
			data = self.data


		fig, axs = plt.subplots(len(cols), figsize = (19.20, 10.80), tight_layout = True)

		colors = color_palette

		for i, col in enumerate(cols):
			temp_data = data[['scrap_date', col]]
			temp_data = temp_data[temp_data[col].notna()]

			ax = axs[i]
			ax.plot(temp_data['scrap_date'], temp_data[col], figure = fig, color=colors[i], linewidth=3)

			first_day = first_day_of_month(datetime(year, month, 1))
			ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday= week_days[first_day] , interval = 1))
			ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))
			ax.xaxis.grid(True, which = "minor")
			ax.yaxis.grid()
			ax.xaxis.set_major_locator(mdates.MonthLocator())
			ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%b\n%Y'))

			title = " ".join(re.findall('[A-Z][^A-Z]*', col))
			ax.set_title('{}'.format(title),size=20)
			ax.tick_params(axis = 'both', which = 'major', labelsize = 18)
			ax.tick_params(axis = 'both', which = 'minor', labelsize = 18)

		for ax in axs:
			ax.label_outer()


		month = datetime(1900, month, 1).strftime('%B')
		fig.suptitle('{} during {}'.format(self.name.capitalize(), month), fontsize=22, fontweight='bold')

		if save:
			title = input('Please enter plots name\n')
			file_format = 'svg'
			fig.savefig('{}\{}.{}'.format(plots_path, title, file_format), format = file_format, edgecolor = 'b',
			bbox_inches ='tight')

		return axs







if __name__ == '__main__':
	new_cols = ['NewCases', 'NewDeaths', 'NewRecovered']
	total_cols = ['TotalCases', 'TotalDeaths', 'TotalRecovered', 'ActiveCases', 'SeriousCritical']
	mpop_cols = ['Tot_Cases_1Mpop', 'Deaths_1Mpop', 'Tests_1Mpop']

	country = Country('USA', 'country')

	country.date_plot(new_cols + ['SeriousCritical'], save = False)

	country.closed_cases_pie(save = False)
	country.monthly_bar(['NewCases', 'NewDeaths', 'NewRecovered','SeriousCritical'], 10, 2020, save = False)

	plt.show()

