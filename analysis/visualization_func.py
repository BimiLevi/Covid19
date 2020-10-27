import calendar
import re

import matplotlib._color_data as mcd
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from resources.paths import plots_path

plt.style.use('classic')
plt.rcParams['font.sans-serif'] = 'Constantia'
plt.rcParams['savefig.dpi'] = 600
plt.rcParams["figure.dpi"] = 100
plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False})
color_palette = {'black': '#3D3D3D', 'blue': '#3F5E99', 'red': '#F04A6B', 'green': '#3AB08B'}

def tableau_colors():
	tab_colors = {}

	for color in mcd.TABLEAU_COLORS:
		tab_colors[color] = mcd.TABLEAU_COLORS[color]

	return tab_colors

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

def month_bar_plot(df, col, cname, month, save = False):
	from analysis.analysis_func import data_by_month

	if month is not None:
		data = data_by_month(df, month)

	else:
		raise ValueError('You must enter the month.')

	data = data[['scrap_date', col]]
	data = data[data[col].notna()]

	fig = plt.figure(figsize = (19.20, 10.80), edgecolor = 'b')
	colors = color_minmax(data, col)

	plot = data[col].plot(kind = 'bar', rot = 0, color = colors, figure = fig)

	plt.tick_params(right = False, top = False)

	days = data['scrap_date'].dt.day.tolist()
	plt.xticks(np.arange(data.shape[0]), days)

	title_list = re.findall('[A-Z][^A-Z]*', col)
	title = " ".join(title_list)
	monthName = calendar.month_name[month]

	plt.xlabel('Days', fontsize = 15, fontweight = 'bold', figure = fig)
	plt.ylabel(title, fontsize = 15, fontweight = 'bold', figure = fig)
	plt.title('{} in {} during {}'.format(title, cname, monthName), fontsize = 17, fontweight = 'bold', figure = fig)

	min_patch = mpatches.Patch(color = '#F04A6B', label = 'Min of ' + title + ' ' + str(data[col].min()))
	max_patch = mpatches.Patch(color = '#3AB08B', label = 'Max of ' + title + ' ' + str(data[col].max()))

	plt.legend(handles = [max_patch, min_patch], bbox_to_anchor = (1.05, 1), loc = "best", frameon = True, edgecolor =
	'black', fontsize = 11)

	if save:
		file_format = 'svg'
		fname = '{} in {} during {}.{}'.format(title, cname, monthName, file_format)
		plt.savefig(plots_path + r'\{}'.format(fname), format = file_format, edgecolor = 'b', bbox_inches = 'tight')

	return plot

def date_plot(ycol, dfs_list, title=None, save = False):
	if len(dfs_list) == 0:
		return 'You need to enter a country or a list of countries.'

	fig = plt.figure(figsize = (19.20, 10.80), tight_layout=True)
	ax = fig.add_subplot()

	colors = tableau_colors()
	colors_list = list(colors.keys())

	for df in dfs_list:
		if 'Country' in df.columns.tolist():
			name = str(df['Country'].unique()[0])

		else:
			name = str(df['Continent'].unique()[0])

		color = colors_list.pop()
		ax.plot(df['scrap_date'], df[ycol], label=name, linewidth=3, color=colors[color])

		handles, labels = ax.get_legend_handles_labels()
		ax.legend(handles, labels, bbox_to_anchor = (1.001, 1), loc = "best", frameon = True, edgecolor ='black',
		          fontsize = 13)


	ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday = 6, interval = 1))
	ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))

	ax.xaxis.grid(True, which = "minor")
	ax.yaxis.grid()
	ax.xaxis.set_major_locator(mdates.MonthLocator())
	ax.xaxis.set_major_formatter(mdates.DateFormatter('\n\n\n%b\n%Y'))

	xtitle = 'Date'
	ytitle = " ".join(re.findall('[A-Z][^A-Z]*', ycol))

	ax.set_xlabel(xtitle, fontsize = 15, fontweight = 'bold')
	ax.set_ylabel(ytitle, fontsize = 15, fontweight = 'bold')
	ax.set_title('{}\n{} by {}'.format(title, ytitle, xtitle), fontsize = 17, fontweight = 'bold')


	for axis in ['bottom', 'left']:
		ax.spines[axis].set_linewidth(2)

	"""Background color"""
	ax.patch.set_facecolor('gray')
	ax.patch.set_alpha(0.1)


	plt.tick_params(right = False, top = False)
	plt.grid(b=True, linewidth=1)



	if save:
		file_format = 'svg'
		fname = '{}.{}'.format(title, file_format)
		plt.savefig(plots_path + r'\{}'.format(fname), format = file_format, edgecolor = 'b', bbox_inches = 'tight')

	return ax


if __name__ == '__main__':
	pass
