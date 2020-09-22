import os

''' In order to use selenium, you need to download webdriver from: https://www.selenium.dev/downloads/,
 after downloading the webdriver add the path in this script.
 '''

webDriver_path = 'C:\Web_drivers\Chromewebdriver\chromedriver.exe'

current_dir = os.getcwd()

utilities_path = current_dir + r'\utilities'
world_path = current_dir + r'\World Meter Data'
countriesID_path = utilities_path + r'\countries id'
continentsID_path = utilities_path + r'\continent id'
mainCountries_path = current_dir + r'\main csvs\main_countries.csv'
mainContinents_path = current_dir + r'\main csvs\main_continents.csv'

def creat_paths():
	from process_func import get_date_parm
	day, month, year = get_date_parm()

	# Crating directories to save the scraped data in them.
	from paths import current_dir
	#  Crating path for each directory.
	dateYea_path = world_path + '/' + year
	dateMon_path = dateYea_path + '/' + month
	dateDay_path = dateMon_path + '/' + day

	dir_paths = [world_path, dateYea_path, dateMon_path, dateDay_path]

	return dir_paths

