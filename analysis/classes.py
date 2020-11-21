import re
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from matplotlib.ticker import FuncFormatter

pio.templates.default = "plotly_dark"
pio.renderers.default = "svg"

from analysis.analysis_func import *
from analysis.visualization_func import *
from database.db_config import current_db as db
from resources.paths import *
from utilities.directories import creat_directory
from utilities.files_function import load_json, calculate_time

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

plt.style.use('classic')
plt.rcParams['font.sans-serif'] = 'Constantia'
plt.rcParams['savefig.dpi'] = 600
plt.rcParams["figure.dpi"] = 100

class Territory:

	def __init__(self, name):
		self.name = name.lower()
		self._data = None

	@calculate_time
	def date_plot(self, cols = [], start_date = None, end_date = None, save = False, ):
		if cols is None:
			cols = ['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered',
		                'ActiveCases', 'SeriousCritical', 'Tot_Cases_1Mpop', 'Deaths_1Mpop', 'TotalTests',
		                'Tests_1Mpop']
		if type(cols) != list:
			raise TypeError('Type must be a list.')

		if len(cols) == 0:
			raise ValueError('cols list is empty.')

		if (start_date is not None) and (end_date is not None):
			data = data_range_date(self._data, start_date, end_date)

		else:
			data = self._data

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
			title = input('For date plot\nPlease enter plots name\n')
			file_format = 'svg'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.savefig('{}\{}.{}'.format(full_path, title, file_format), format = file_format,
			            edgecolor = 'b',bbox_inches ='tight')

		return ax

	@calculate_time
	def closed_cases_pie(self, save = False):
		fig, ax = plt.subplots(figsize = (19.20, 10.80), tight_layout = True)

		cases = self._data[self._data['scrap_date'] == self._data['scrap_date'].max()]
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
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.savefig('{}\{}.{}'.format(full_path, title, file_format), format = file_format, edgecolor = 'b',bbox_inches ='tight')


		return pie

	@calculate_time
	def monthly_plot(self, cols, month, year, save = False):
		if len(cols) > 4:
			raise ValueError('The maximum amount of columns is 4.')

		if month is not None:
			data = data_by_month(self._data, month, year)

		else:
			data = self._data

		fig, axs = plt.subplots(len(cols), figsize = (19.20, 10.80), tight_layout = True)

		colors = color_palette

		for i, col in enumerate(cols):
			temp_data = data[['scrap_date', col]]
			temp_data = temp_data[temp_data[col].notna()]

			if len(cols) == 1:
				ax = axs

			else:
				ax = axs[i]

			ax.plot(temp_data['scrap_date'], temp_data[col], figure = fig, color=colors[i], linewidth=3)

			first_day = first_day_of_month(datetime(year, month, 1))
			ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday= week_days[first_day], interval = 1))
			ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))
			ax.xaxis.grid(True, which = "minor")
			ax.yaxis.grid()
			ax.xaxis.set_major_locator(mdates.MonthLocator())
			ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%b\n%Y'))

			title = " ".join(re.findall('[A-Z][^A-Z]*', col))
			ax.set_title('{}'.format(title),size=20)
			ax.tick_params(axis = 'both', which = 'major', labelsize = 18)
			ax.tick_params(axis = 'both', which = 'minor', labelsize = 18)

			ax.spines['right'].set_visible(False)
			ax.spines['top'].set_visible(False)

		month = datetime(1900, month, 1).strftime('%B')
		fig.suptitle('{} during {}'.format(self.name.capitalize(), month), fontsize=22, fontweight='bold')

		if save:
			title = input('For monthly plot \n Please enter plots name\n'.format())
			file_format = 'svg'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.savefig('{}\{}.{}'.format(full_path,title, file_format), format = file_format, edgecolor = 'b',
			            bbox_inches ='tight')

		return ax

	@calculate_time
	def daily_increase(self, col, save = False):
		df = self._data
		df['sma'] = df[col].rolling(window = 7).mean()

		fig, ax = plt.subplots(figsize = (19.20, 10.80), tight_layout = True)
		ax2 = ax.twinx()

		fig.suptitle('{}\nDaily increase of {}'.format(self.name.capitalize(), col), size = 20)

		ax.bar(df['scrap_date'], df[col], color='orange')

		ax2.plot(df['scrap_date'], df['sma'], color = 'lightcoral', marker = 'o', linestyle = 'dashed', linewidth = 3,
		         label = '7 days moving avg')

		ax.set_ylabel(col, size = 20)
		ax.tick_params(axis = 'both', which = 'major', labelsize = 20)
		ax.tick_params(axis = 'x', which = 'minor', labelsize = 18)
		ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday = 6, interval = 1))
		ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))
		ax.xaxis.grid(True, which = "minor")
		ax.yaxis.grid()
		ax.xaxis.set_major_locator(mdates.MonthLocator())
		ax.xaxis.set_major_formatter(mdates.DateFormatter('\n\n\n%b\n%Y'))

		ax2.tick_params(axis = 'y', labelsize = 18)
		ax2.axis('off')
		handles, labels = ax2.get_legend_handles_labels()
		ax.legend(handles, labels, bbox_to_anchor = (1.001, 1), loc = "best", frameon = True, edgecolor = 'black',
		          fontsize = 15)
		if save:
			title = 'Daily increase of {} in {}'.format(col, self.name)
			file_format = 'svg'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.savefig('{}\{}.{}'.format(full_path, title, file_format), format = file_format,
			            edgecolor = 'b', bbox_inches ='tight')


		return fig

	def case_fatality_ratio(self):
		cfr = self._data['TotalDeaths'].sum()/(self._data['TotalDeaths'].sum()+self._data['TotalRecovered'].sum())
		cfr = round(cfr * 100, 3)
		return cfr

	def linear_plot(self, y_cols):
		fig = px.line(self._data, x='scrap_date', y=y_cols,
		              title="{} Cumulative\Active Cases Over Time".format(self.name.capitalize()),
		              labels={'scrap_date': 'Date'}, color='variable')
		return fig

	def boxplot(self, col, save = False):
		if not col in ['NewCases','NewDeaths', 'NewRecovered']:
			print('{} is is unknown'.format(col))
			return False

		elif type(col) != str:
			raise TypeError('{} must be of str type'.format(col))

		else:
			fig = px.box(self._data, y= col)
			fig.update_traces(quartilemethod = "exclusive")

			if save:
				title = 'Boxplot of {} in {}'.format(col, self.name)
				file_format = 'svg'
				full_path = os.path.join(plots_path, self.name)
				if not os.path.isfile(full_path):
					creat_directory(full_path)
				fig.write_image('{}\{}.{}'.format(full_path, title, file_format))

			return fig


class Country(Territory):
	def __init__(self, name):
		super().__init__(name)

		self.ttype = 'country'
		self.__data = db.get_table(self.name)

		self.id = self.__data['Country_id'].unique()[0]
		self.code = get_alpha_3(self.name)

		temp = pd.DataFrame(load_json(countries_path))
		self.continent_id = int(temp[temp['Country_id'] == self.id]['Continent_id'].unique()[0])

		temp = load_json(continents_path)
		temp = dict([(value, key) for key, value in temp.items()])
		self.continent = temp[self.continent_id]
		del temp

		self.population = self.__data['Population'][0]
		self.last_update = self.__data['scrap_date'].max().date()
		self.first_update = self.__data['scrap_date'].min().date()

		self._data = self.__data.drop(columns =['Population', 'update_time_GMT', 'Country_id', 'Country'])

		self.size = self.__data.shape
		self.columns = self.__data.columns.tolist()

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

	@property
	def data(self):
		return self.__data

	@data.setter
	def data(self, table):
		self.__data = db.get_table(table)

	# TODO: fix the method.
	@staticmethod
	def world_map():
		df = db.get_table('All countries updated')
		df['iso_alpha'] = df['Country'].map(lambda row: get_alpha_3(row))

class Continent(Territory):
	def __init__(self, name):
		super().__init__(name)

		self.ttype = 'continent'

		self.__data = db.get_table(self.name)
		self.id = self.__data['Continent_id'].unique()[0]
		self.last_update = self.__data['scrap_date'].max().date()
		self.first_update = self.__data['scrap_date'].min().date()

		self.__data = self.__data.drop(columns =['update_time_GMT', 'Continent_id', 'Continent'])

		self.size = self.__data.shape
		self.columns = self.__data.columns.tolist()

	def __str__(self):
		return """
Continent name: {}
Continents id: {}
First update: {}
Last update: {}
Data number of rows: {}
Data number of columns: {}
Columns: \n{}
		""".format(self.name.capitalize(), self.id, self.first_update, self.last_update, self.size[0], self.size[1], self.columns)

	@property
	def data(self):
		return self.__data

	@data.setter
	def data(self, table):
		self.__data = db.get_table(table)

class Top:
	def __init__(self, ttype, limit = 10):
		self.ttype = ttype
		self.__limit = limit

		if ttype == 'countries':
			self.col_type = 'Country'
			self.data = db.get_table('All countries updated')


		elif ttype == 'continents':
			self.col_type = 'Continent'
			self.data = db.get_table('All continents updated')

		else:
			print("Couldn't Identify the requested territory")
			raise FileNotFoundError()

		self.obj_dict = {}

	def __str__(self):
		return """
Territory type: {}
Limit: {}
		""".format(self.ttype, self.limit)

	@property
	def limit(self):
		return self.__limit

	@limit.setter
	def limit(self, new_limit):
		self.__limit = new_limit

	def set_obj(self, df):
		for name in df[self.col_type]:

			if self.ttype == 'countries':
				self.obj_dict[name] = Country(name)

			elif self.ttype == 'continents':
				self.obj_dict[name] = Continent(name)

	def sort_limit_data(self, col):
		sorted_data = self.data.dropna().sort_values(by = col).reset_index(drop = True).tail(self.limit)
		sorted_data.index = np.arange(1, len(sorted_data) + 1)

		self.set_obj(sorted_data)
		return sorted_data

	@calculate_time
	def top_bar(self, col, save = None):

		data = self.sort_limit_data(col)
		colors = color_minmax(data, col)

		fig, axs = plt.subplots(figsize = (19.20, 10.80), tight_layout = True)
		bar = axs.bar(data[self.col_type], data[col], width=0.8, color=colors)


		min_max = get_minmax(data, col)
		for index, value in min_max.items():
			value = round(value, 1)
			axs.text(index - 1, value * 1.005, f'{value:,}', fontsize = 14, ha = 'center', fontweight = 'bold')

		formatter = FuncFormatter(MK_formatter)
		axs.yaxis.set_major_formatter(formatter)

		axs.set_xlabel(self.col_type)
		axs.set_ylabel('Values')
		axs.set_title('Top {} {}\nby {}'.format(self.limit, self.ttype,col))

		if save:
			title = 'Top {} {} {}'.format(len(data),self.ttype,col)
			file_format = 'svg'
			full_path = os.path.join(plots_path, 'top')
			if not os.path.isfile(full_path):
				creat_directory(full_path)

			fig.savefig('{}\{} bar plot.{}'.format(full_path, title, file_format), format = file_format, edgecolor = 'b',
			 bbox_inches = 'tight')
		return bar

	@calculate_time
	def top_line(self, col, save = None):
		names_list = self.sort_limit_data(col)[self.col_type].to_list()

		fig, ax = plt.subplots(figsize = (19.20, 10.80), tight_layout = True)

		for i, table in enumerate(self.obj_dict.values()):
			ax.plot(table.data['scrap_date'], table.data[col], linewidth=3, label = table.name.capitalize(),
			        color=color_palette[i])

		ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday = 6, interval = 1))
		ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))

		formatter = FuncFormatter(MK_formatter)
		ax.yaxis.set_major_formatter(formatter)

		ax.xaxis.grid(True, which = "minor")
		ax.yaxis.grid()
		ax.xaxis.set_major_locator(mdates.MonthLocator())
		ax.xaxis.set_major_formatter(mdates.DateFormatter('\n\n\n%b\n%Y'))

		xtitle = 'Date'
		ytitle = 'Values'

		ax.set_xlabel(xtitle,fontsize = 15, fontweight = 'bold')
		ax.set_ylabel(ytitle,fontsize = 15, fontweight = 'bold')
		ax.set_title('Top {} {}\nby {}'.format(self.limit, self.ttype, col))

		handles, labels = ax.get_legend_handles_labels()
		ax.legend(handles, labels, bbox_to_anchor = (1.001, 1), loc = "best", frameon = True, edgecolor = 'black',
		          fontsize = 20)

		if save:
			title = 'Top {} {} {}'.format(len(names_list), self.ttype, col)
			file_format = 'svg'
			full_path = os.path.join(plots_path, 'top')
			if not os.path.isfile(full_path):
				creat_directory(full_path)

			fig.savefig('{}\{} line plot.{}'.format(full_path, title, file_format), format = file_format, edgecolor =
			'b',
			 bbox_inches = 'tight')
		return ax

	# TODO: Requires another check.
	@calculate_time
	def get_map(self, col):
		from analysis.visualization_func import countries_map

		df = self.sort_limit_data(col)[[self.col_type, col]]
		countries_loc = {}

		for obj_name in self.obj_dict.keys():
			location = geolocate(obj_name)
			countries_loc[obj_name] = location

		df['location'] = df[self.col_type].map(countries_loc)
		df[['Latitude', 'Longitude']] = pd.DataFrame(df['location'].tolist(), index=df.index)
		df = df.drop(columns = ['location'])

		title = 'Top {} {} With the highest {}'.format(len(df), self.ttype, col)

		countries_map(df, title, col)

if __name__ == '__main__':
	top = Top('countries')
	country = Country('israel')
	# fig = country.linear_plot(['TotalCases', 'TotalDeaths','TotalRecovered','ActiveCases'])
	fig = country.boxplot('NewCases', save=False)

	fig.show()
	# plt.show()





