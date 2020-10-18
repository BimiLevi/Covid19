import os

project_path = os.path.dirname(os.path.dirname(__file__))

site_url = "https://www.worldometers.info/coronavirus"

world_path = os.path.join(project_path, 'World Meter Data')
utilities_path = os.path.join(project_path, 'utilities')
resources_path = os.path.join(project_path, 'resources')

countries_path = os.path.join(resources_path, 'Countries table')
continents_path = os.path.join(resources_path, 'Continents table')
countries_id = os.path.join(resources_path, 'Countries id')

def creat_paths():
	from scraper.process_func import get_date_parm

	day, month, year = get_date_parm()

	# Crating directories to save the scraped data in them.
	#  Crating path for each directory.
	dateYea_path = world_path + '/' + year
	dateMon_path = dateYea_path + '/' + month
	dateDay_path = dateMon_path + '/' + day

	dir_paths = [world_path, dateYea_path, dateMon_path, dateDay_path]

	return dir_paths


