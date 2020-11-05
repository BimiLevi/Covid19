import matplotlib._color_data as mcd

color_dict = {'black': '#3D3D3D', 'blue': '#3F5E99', 'red': '#F04A6B', 'green': '#3AB08B'}
color_palette = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', '#3AB08B', '#F04A6B', '#3F5E99', '#3D3D3D',
                 '#FFC107','#651FFF']

week_days = {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7}


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
			colors.append(color_dict['green'])
		elif val == min_val:
			colors.append(color_dict['red'])
		else:
			colors.append(color_dict['blue'])
	return colors


def MK_formatter(x, pos):
	'The two args are the value and tick position'
	if x >= 1e6:
		return '%1.2fM' % (x * 1e-6)
	else:
		return '%1.3fK' % (x * 1e-3)





if __name__ == '__main__':
	pass
