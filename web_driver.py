from selenium import webdriver
from paths import webDriver_path

'''
    OR: Exception Handling!!! expcially here in WebDrivers
'''
class Driver:
	def __init__(self):
		self.driver = webdriver.Chrome(executable_path = webDriver_path)
