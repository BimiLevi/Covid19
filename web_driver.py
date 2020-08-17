from selenium import webdriver

class Driver:
	def __init__(self):
		path = 'C:\Web_drivers\Chromewebdriver\chromedriver.exe'
		self.driver = webdriver.Chrome(executable_path=path)
