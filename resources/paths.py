import os
import datetime

project_path = os.path.dirname(os.path.dirname(__file__))

site_url = "https://www.worldometers.info/coronavirus"

data_path = os.path.join(project_path, 'data')
Dtables_path = os.path.join(data_path, 'tables')
Ddate_path = os.path.join(data_path, 'date')

utilities_path = os.path.join(project_path, 'utilities')
resources_path = os.path.join(project_path, 'resources')

countries_path = os.path.join(resources_path, 'Countries table')
continents_path = os.path.join(resources_path, 'Continents table')
countries_id = os.path.join(resources_path, 'Countries id')

analysis_path = os.path.join(project_path, 'analysis')
plots_path = os.path.join(analysis_path, 'plots')

countriesCodes_path = os.path.join(resources_path, 'countries codes')

def create_paths(yesterday = False):
	today = datetime.datetime.today().date()
	if yesterday:
		date = today - datetime.timedelta(days = 1)

	else:
		date = today

	# Crating directories to save the scraped data in them.
	# Crating path for each directory.
	dateYea_path = Ddate_path + '/' + date.strftime("%Y")
	dateMon_path = dateYea_path + '/' + date.strftime("%B")
	dateDay_path = dateMon_path + '/' + date.strftime("%d")


	dir_paths = [Ddate_path, dateYea_path, dateMon_path, dateDay_path]

	return dir_paths


