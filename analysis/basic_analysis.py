import pandas as pd

from database.db_config import current_db

db = current_db



israel = pd.read_sql('Israel', con = db.get_engine())

# temp_list = ['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths','TotalRecovered','NewRecovered','ActiveCases',
#              'SeriousCritical']
# for col in temp_list:
# 	month_bar_plot(israel, col, 'Israel', month = 9, save = True)
# 	plt.show()

