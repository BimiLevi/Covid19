from selenium import webdriver
from resources.paths import webDriver_path


class Driver:
	def __init__(self):
		self.driver = webdriver.Chrome(executable_path = webDriver_path)
