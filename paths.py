import os

''' In order to use selenium, you need to download webdriver from: https://www.selenium.dev/downloads/,
 after downloading the webdriver add the path in this script.
 '''

webDriver_path = 'C:\Web_drivers\Chromewebdriver\chromedriver.exe'

current_dir = os.getcwd()

utilities_path = current_dir + r'\utilities'
countriesID_path = utilities_path + r'\countries id'
continentsID_path = utilities_path + r'\continent id'
allCountries_path = current_dir + r'\main csvs\main_countries.csv'
allContinents_path = current_dir + r'\main csvs\main_continents.csv'


