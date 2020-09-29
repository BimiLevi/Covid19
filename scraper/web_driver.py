from selenium import webdriver
from resources.paths import webDriver_path


class Driver:
	try:
		def __init__(self):
			self.driver = webdriver.Chrome(executable_path = webDriver_path)

	except Exception as e:
		print("Couldn't use the web driver, try to check the version of the driver or the type of browser.")
		raise e
