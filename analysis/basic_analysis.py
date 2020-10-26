from database.db_config import current_db as db

israel = db.get_table('Israel')
us = db.get_table('USA')
uk = db.get_table('UK')

print(uk.columns.tolist())
# temp_list = ['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths','TotalRecovered','NewRecovered','ActiveCases',
#              'SeriousCritical']
# for col in temp_list:
# 	month_bar_plot(israel, col, 'Israel', month = 9, save = True)
# 	plt.show()

