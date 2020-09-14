import os

''' In order to use selenium, you need to download webdriver from: https://www.selenium.dev/downloads/,
 after downloading the webdriver add the path in this script.
 '''

'''
OR: Use Enviornment Variables
'''
webDriver_path = 'C:\web_driver\chromedriver.exe'

current_dir = os.getcwd()

utilities_path = current_dir + r'\utilities'
countriesID_path = utilities_path + r'\countries id'
continentsID_path = utilities_path + r'\continent id'
allCountries_path = current_dir + r'\all data csvs\all_data_countries.csv'
allContinents_path = current_dir + r'\all data csvs\all_data_continents.csv'


