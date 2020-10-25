import calendar
import re

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from resources.paths import plots_path

plt.style.use('classic')
plt.rcParams['font.sans-serif'] = 'Constantia'
plt.rcParams['savefig.dpi'] = 600
plt.rcParams["figure.dpi"] = 100
plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False})
color_palette = {'black': '#3D3D3D', 'blue': '#3F5E99', 'yellow': '#EBCA88', 'red': '#F04A6B', 'green': '#3AB08B'}

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

	fig = plt.figure(figsize=(19.20, 10.80), edgecolor = 'b')
	colors = color_minmax(data, col)

	plot = data[col].plot(kind='bar', rot=0, color=colors, figure=fig)

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

	plt.legend(handles=[max_patch, min_patch], bbox_to_anchor=(1.05, 1), loc= "best", frameon = True, edgecolor=
	'black',
	           fontsize = 11)

	if save:
		file_format = 'svg'
		fname = '{} in {} during {}.{}'.format(title, cname, monthName, file_format)
		plt.savefig(plots_path + r'\{}'.format(fname), format=file_format, edgecolor='b', bbox_inches='tight')

	return plot