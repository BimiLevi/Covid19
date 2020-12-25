import re
from datetime import datetime, date

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from matplotlib.ticker import FuncFormatter

from analysis.analysis_func import *
from analysis.visualization_func import *
from database.db_config import current_db as db
from resources.paths import *
from utilities.directories import creat_directory
from utilities.files_function import load_json, calculate_time

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None

pio.templates.default = "plotly_dark"
# pio.renderers.default = "svg" # Disables the hovermode
# pio.renderers.default = "browser"
color_platte_dark = {'blue': '#9FCEF6', 'white': '#F4F2F7', 'red': '#F20505', 'green': '#B5F88F', 'yellow': '#F2BD1D',
                     'purple': '#A6036D', 'orange': '#F27830', 'pink': '#FBA9B4'}
plt.style.use('classic')
plt.rcParams['font.sans-serif'] = 'Constantia'
plt.rcParams['savefig.dpi'] = 600
plt.rcParams["figure.dpi"] = 100


class Territory:
	# TODO: Change the plots font
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

			ax.plot(data['Date'], values, linewidth = 3, label = col_title, color = color_palette[i])

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
			            edgecolor = 'b', bbox_inches = 'tight')

		return ax

	@calculate_time
	def closed_cases_pie(self, save = False):
		fig, ax = plt.subplots(figsize = (19.20, 10.80), tight_layout = True)

		cases = self._data[self._data['Date'] == self._data['Date'].max()]
		cases = cases[['TotalCases', 'ActiveCases', 'TotalRecovered', 'TotalDeaths']]

		nclosed = (cases['TotalCases'] - cases['ActiveCases']).tolist()[0]

		ratio = cases[['TotalRecovered', 'TotalDeaths']] / nclosed
		idx = ratio.index

		t_ratio = ratio.T.rename(columns = {idx[0]: 'x'})

		labels = ratio.columns.tolist()
		colors = ['tab:green', 'tab:red']

		wedges, _ = ax.pie(t_ratio['x'], labels = labels, startangle = 90, pctdistance = 0.85,
		                   colors = colors, normalize = True, textprops = {'fontsize': 20})
		plt.setp(wedges, width = 0.3, edgecolor = 'black')
		legend_labels = round(t_ratio['x'] * 100, 3).astype(str) + '%'
		ax.legend(wedges, legend_labels, loc = "center left", bbox_to_anchor = (1, 0, 0.5, 1), prop = {'size': 20})
		ax.set_title('{} Closed Cases Ratio'.format(self.name.capitalize()), fontsize = 25, fontweight = 'bold')

		if save:
			title = '{} Closed Cases Ratio'.format(self.name.capitalize())
			file_format = 'svg'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.savefig('{}\{}.{}'.format(full_path, title, file_format), format = file_format, edgecolor = 'b',
			            bbox_inches = 'tight')

		return zip(wedges, _)

	def monthly_plot(self, cols, month, year, save = False):
		if len(cols) > 4:
			raise ValueError('The maximum amount of columns is 4.')

		if month is not None:
			data = data_by_month(self._data, month, year)

		else:
			data = self._data

		fig, axs = plt.subplots(len(cols), figsize = (19.20, 13.80), tight_layout = True)

		colors = color_palette

		for i, col in enumerate(cols):
			temp_data = data[['Date', col]]
			temp_data = temp_data[temp_data[col].notna()]

			if len(cols) == 1:
				ax = axs

			else:
				ax = axs[i]

			ax.plot(temp_data['Date'], temp_data[col], figure = fig, color = colors[i], linewidth = 3)

			first_day = first_day_of_month(datetime(year, month, 1))
			ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday = week_days[first_day], interval = 1))
			ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))
			ax.xaxis.grid(True, which = "minor")
			ax.yaxis.grid()
			ax.xaxis.set_major_locator(mdates.MonthLocator())
			ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%b\n%Y'))

			title = " ".join(re.findall('[A-Z][^A-Z]*', col))
			ax.set_title('{}'.format(title), size = 20)
			ax.tick_params(axis = 'both', which = 'major', labelsize = 16)
			ax.tick_params(axis = 'both', which = 'minor', labelsize = 16)

			ax.spines['right'].set_visible(False)
			ax.spines['top'].set_visible(False)

		month = datetime(1900, month, 1).strftime('%B')
		fig.suptitle('{} during {}'.format(self.name.capitalize(), month), fontsize = 22, fontweight = 'bold')

		if save:
			title = f'{self.name.capitalize()} in {month}'
			file_format = 'svg'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.savefig('{}\{}.{}'.format(full_path, title, file_format), format = file_format, edgecolor = 'b',
			            bbox_inches = 'tight')

		return ax

	# Matplotlib
	@calculate_time
	def daily_increase(self, col, save = False):
		df = self._data
		df['sma'] = df[col].rolling(window = 7).mean()

		fig, ax = plt.subplots(figsize = (19.20, 10.80), tight_layout = True)
		ax2 = ax.twinx()

		fig.suptitle('{}\nDaily increase of {}'.format(self.name.capitalize(), col), size = 20)

		ax.bar(df['Date'], df[col], color = 'orange')

		ax2.plot(df['Date'], df['sma'], color = 'lightcoral', marker = 'o', linestyle = 'dashed', linewidth = 3,
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
			            edgecolor = 'b', bbox_inches = 'tight')

		return fig

	# Plotly
	def daily_increase2(self, col, save = False):
		df = self._data[['Date', col]]
		df['sma'] = df[col].rolling(window = 7).mean()
		df = df[df[col].isnull() == False]

		fig = go.Figure()

		fig.add_trace(go.Bar(name = f"{col} ", x = df['Date'], y = df[col]))
		fig.update_traces(marker_color = color_platte_dark["purple"])

		fig.add_trace(
			go.Scatter(name = '7 Days Moving Avg', x = df['Date'], y = df['sma'], mode = 'lines+markers',
			           line_color = color_platte_dark['orange']))

		fig.update_xaxes(type = 'date', tick0 = df['Date'].iloc[0], dtick = 86400000.0 * 7,
		                 ticklabelmode = 'period',
		                 rangeslider_visible = True)

		fig.update_layout(
				title = '{}\nDaily increase of {}'.format(self.name.capitalize(), col) + '<br>' "<span " \
				                                                                         "style='font-size:12px;'>Creation date {}</span>".format(
					date.today()),
				autosize = False,
				xaxis_tickformat = "%d\n%b",
				xaxis_title = 'Date',
				yaxis_title = f'{col}',
				)

		if save:
			title = f'Daily increase of {col} in {self.name.capitalize()}'
			file_format = 'html'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.write_html('{}\{}.{}'.format(full_path, title, file_format))

		return fig

	def daily_increase3(self, save = False):
		df = self._data
		df['activeCases_sma'] = df['ActiveCases'].rolling(window = 7).mean()
		df['NewCases_sma'] = df['NewCases'].rolling(window = 7).mean()
		df['NewDeaths_sma'] = df['NewDeaths'].rolling(window = 7).mean()
		df['NewRecovered_sma'] = df['NewRecovered'].rolling(window = 7).mean()
		x = self._data['Date']

		fig = go.Figure(data = [
			go.Bar(
					name = 'Active Cases',
					x = x,
					y = self._data['ActiveCases'],
					marker_color = color_platte_dark['yellow']
					),
			go.Bar(
					name = 'New Cases',
					x = x,
					y = self._data['NewCases'],
					marker_color = color_platte_dark['orange'],
					visible = 'legendonly'
					),
			go.Bar(
					name = 'New Deaths',
					x = x,
					y = self._data['NewDeaths'],
					marker_color = color_platte_dark['red'],
					visible = 'legendonly'
					),
			go.Bar(
					name = 'New Recovered',
					x = x,
					y = self._data['NewRecovered'],
					marker_color = color_platte_dark['green'],
					visible = 'legendonly'
					),
			go.Scatter(
					name = 'Active Cases 7 days moving avg',
					x = x,
					y = self._data['activeCases_sma'],
					line = dict(color = color_platte_dark['purple']),
					mode = 'lines+markers'
					),
			go.Scatter(
					name = 'New Cases 7 days moving avg',
					x = x,
					y = self._data['NewCases_sma'],
					line = dict(color = color_platte_dark['pink']),
					mode = 'lines+markers',
					visible = 'legendonly'
					),
			go.Scatter(
					name = 'New Deaths 7 days moving avg',
					x = x,
					y = self._data['NewDeaths_sma'],
					line = dict(color = color_platte_dark['blue']),
					mode = 'lines+markers',
					visible = 'legendonly'
					),
			go.Scatter(
					name = 'New Recovered 7 days moving avg',
					x = x,
					y = self._data['NewRecovered_sma'],
					line = dict(color = color_platte_dark['white']),
					mode = 'lines+markers',
					visible = 'legendonly'
					)
			])

		fig.update_layout(
				title = f"{self.name.capitalize()}  Daily increase of Active Cases" + "<br>" + "<span " \
				                                                                               f"style='font-size:12px;'>Creation date {date.today()}</span>",
				autosize = False,
				xaxis_tickformat = "%d\n%b",
				xaxis_title = 'Date',
				yaxis_title = 'Value',
				width = 1000,
				height = 800,
				)
		fig.layout.update(go.Layout(barmode = 'overlay', ))

		fig.update_xaxes(type = 'date', tick0 = df['Date'].iloc[0], dtick = 86400000.0 * 7,
		                 ticklabelmode = 'period',
		                 rangeslider_visible = True,
		                 tickangle = 0)

		if save:
			title = f'{self.name.capitalize()} Daily increase'
			file_format = 'html'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.write_html('{}\{}.{}'.format(full_path, title, file_format))

		return fig

	def case_fatality_ratio(self):
		cfr = self._data['TotalDeaths'].sum() / (self._data['TotalDeaths'].sum() + self._data['TotalRecovered'].sum())
		cfr = round(cfr * 100, 3)
		return cfr

	def linear_plot(self, y_cols, save = False):
		x = self._data['Date']
		fig = go.Figure(data = [
			go.Scatter(
					name = 'Active Cases',
					x = x,
					y = self._data['ActiveCases'],
					line = dict(color = color_platte_dark['yellow'])
					),
			go.Scatter(
					name = 'Total Cases',
					x = x,
					y = self._data['TotalCases'],
					line = dict(color = color_platte_dark['orange'])
					),
			go.Scatter(
					name = 'Total Deaths',
					x = x,
					y = self._data['TotalDeaths'],
					line = dict(color = color_platte_dark['red'])

					),
			go.Scatter(
					name = 'Total Recovered',
					x = x,
					y = self._data['TotalRecovered'],
					line = dict(color = color_platte_dark['green'])

					)
			])

		fig.update_xaxes(type = 'date', tick0 = self._data['Date'].iloc[0], dtick = 86400000.0 * 7,
		                 ticklabelmode = 'period')

		fig.update_layout(
				title = f"{self.name.capitalize()} Cumulative\Active Cases Over Time" + "<br>" + "<span " \
				                                                                                 f"style='font-size:12px;'>Creation date {date.today()}</span>",
				autosize = False,
				width = 900,
				xaxis_tickformat = "%d\n%b",
				xaxis_title = 'Date',
				yaxis_title = 'Value',
				hovermode = 'x unified',
				updatemenus = [
					dict(
							active = 0,
							buttons = list([
								dict(label = "All",
								     method = "update",
								     args = [{"visible": [True, True, True, True]},
								             {
									             "title": f"{self.name.capitalize()} Cumulative\Active Cases Over Time" + "<br>" + "<span " \
									                                                                                               f"style='font-size:12px;'>Creation date {date.today()}</span>"}]),

								dict(label = "Active Cases",
								     method = "update",
								     args = [{"visible": [True, False, False, False]},
								             {
									             "title": f"{self.name.capitalize()} Active Cases Over Time" + "<br>" + "<span " \
									                                                                                    f"style='font-size:12px;'>Creation date {date.today()}</span>",
									             }]),

								dict(label = "Total Cases",
								     method = "update",
								     args = [{"visible": [False, True, False, False]},
								             {"title": f"{self.name.capitalize()} Total Cases Over Time" + "<br>" +
								                       "<span " \
								                       f"style='font-size:12px;'>Creation date {date.today()}</span>",
								              }]),

								dict(label = "Total Deaths",
								     method = "update",
								     args = [{"visible": [False, False, True, False]},
								             {"title": f"{self.name.capitalize()} Total Deaths Over Time" + "<br>" +
								                       "<span " \
								                       f"style='font-size:12px;'>Creation date {date.today()}</span>",
								              }]),

								dict(label = "Total Recovered",
								     method = "update",
								     args = [{"visible": [False, False, False, True]},
								             {"title": f"{self.name.capitalize()} Total Recovered Over Time" + "<br>" +
								                       "<span " \
								                       f"style='font-size:12px;'>Creation date {date.today()}</span>",
								              }])
								]),
							)
					])

		if save:
			title = 'Line plot of {} in {}'.format(",".join(y_cols), self.name)
			file_format = 'html'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.write_html('{}\{}.{}'.format(full_path, title, file_format))

		return fig

	def boxplot(self, cols, save = False):
		for col in cols:
			if not col in ['NewCases', 'NewDeaths', 'NewRecovered', 'ActiveCases']:
				print('{} is  unknown'.format(cols))
				raise ValueError('{} is unknown'.format(cols))

			elif type(col) != str:
				raise TypeError('{} must be of str type'.format(cols))

		fig = px.box(self._data, y = cols, title = "{} Boxplot for {}".format(
				self.name.capitalize(),
				cols) + "<br>" + "<span style='font-size: 12px;'>Creation date {}</span>".format(
				date.today()))
		fig.update_traces(quartilemethod = "exclusive")

		if save:
			title = 'Boxplot of {} in {}'.format(cols, self.name)
			file_format = 'html'
			full_path = os.path.join(plots_path, self.name)
			if not os.path.isfile(full_path):
				creat_directory(full_path)
			fig.write_html('{}\{}.{}'.format(full_path, title, file_format))

			return fig

	def three_months_info(self):
		group_df = self._data.groupby(by = [self._data['Date'].dt.year,
		                                    self._data['Date'].dt.month]).agg(
				ActiveCasesAvg = ('ActiveCases', 'mean'),
				RecoveredSum = ('NewRecovered', 'sum'),
				DeathsSum = ('NewDeaths', 'sum'),
				CasesSum = ('NewCases', 'sum'),
				CriticalSum = ('SeriousCritical', 'sum'))

		group_df = pd.DataFrame(group_df).tail(4).iloc[:3]
		group_df = group_df.rename_axis(['Year', 'Month']).reset_index()

		group_df['ActiveCasesAvg'] = group_df['ActiveCasesAvg'].astype('float64')
		group_df['ActiveCasesAvg'] = group_df['ActiveCasesAvg'].apply(lambda x: "{:,.3f}".format(x))
		group_df['RecoveredSum'] = group_df['RecoveredSum'].apply(lambda x: "{:,.0f}".format(x))
		group_df['DeathsSum'] = group_df['DeathsSum'].apply(lambda x: "{:,.0f}".format(x))
		group_df['CasesSum'] = group_df['CasesSum'].apply(lambda x: "{:,.0f}".format(x))
		group_df['CriticalSum'] = group_df['CriticalSum'].apply(lambda x: "{:,.0f}".format(x))

		group_df['Month'] = group_df['Month'].apply(lambda x: calendar.month_abbr[x])

		return group_df


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
		self.last_update = self.__data['Date'].max().date()
		self.first_update = self.__data['Date'].min().date()

		self._data = self.__data.drop(columns = ['Population', 'Update_time_GMT', 'Country_id', 'Country'])

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
		self.last_update = self.__data['Date'].max().date()
		self.first_update = self.__data['Date'].min().date()

		self.__data = self.__data.drop(columns = ['Update_time_GMT', 'Continent_id', 'Continent'])

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
		""".format(self.name.capitalize(), self.id, self.first_update, self.last_update, self.size[0], self.size[1],
		           self.columns)

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
		bar = axs.bar(data[self.col_type], data[col], width = 0.8, color = colors)

		min_max = get_minmax(data, col)
		for index, value in min_max.items():
			value = round(value, 1)
			axs.text(index - 1, value * 1.005, f'{value:,}', fontsize = 14, ha = 'center', fontweight = 'bold')

		formatter = FuncFormatter(MK_formatter)
		axs.yaxis.set_major_formatter(formatter)

		axs.set_xlabel(self.col_type)
		axs.set_ylabel('Values')
		axs.set_title('Top {} {}\nby {}'.format(self.limit, self.ttype, col))

		if save:
			title = 'Top {} {} {}'.format(len(data), self.ttype, col)
			file_format = 'svg'
			full_path = os.path.join(plots_path, 'top')
			if not os.path.isfile(full_path):
				creat_directory(full_path)

			fig.savefig('{}\{} bar plot.{}'.format(full_path, title, file_format), format = file_format,
			            edgecolor = 'b',
			            bbox_inches = 'tight')
		return bar

	@calculate_time
	def top_line(self, col, save = None):
		names_list = self.sort_limit_data(col)[self.col_type].to_list()

		fig, ax = plt.subplots(figsize = (19.20, 10.80), tight_layout = True)

		for i, table in enumerate(self.obj_dict.values()):
			ax.plot(table.data['Date'], table.data[col], linewidth = 3, label = table.name.capitalize(),
			        color = color_palette[i])

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

		ax.set_xlabel(xtitle, fontsize = 15, fontweight = 'bold')
		ax.set_ylabel(ytitle, fontsize = 15, fontweight = 'bold')
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
		df[['Latitude', 'Longitude']] = pd.DataFrame(df['location'].tolist(), index = df.index)
		df = df.drop(columns = ['location'])

		title = 'Top {} {} With the highest {}'.format(len(df), self.ttype, col)

		countries_map(df, title, col)


if __name__ == '__main__':
	top = Top('countries')
	country = Country('israel')
	measures = ['ActiveCases', 'NewCases', 'NewRecovered', 'NewDeaths']

# pie = country.closed_cases_pie(save = True)
# month = country.monthly_plot(measures,11,2020,save = True)
# fig = country.boxplot(measures, save = True)
# fig = country.daily_increase2('ActiveCases')
# fig.show()
# plt.show()
