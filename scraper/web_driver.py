from selenium import webdriver
from resources.paths import webDriver_path


class Driver:
	try:
		def __init__(self):
			options = webdriver.ChromeOptions()
			options.add_argument('--ignore-certificate-errors')
			options.add_argument('--ignore-ssl-errors')

			caps = webdriver.DesiredCapabilities.CHROME.copy()
			caps['acceptInsecureCerts'] = True
			caps['acceptSslCerts'] = True

			self.driver = webdriver.Chrome(executable_path = webDriver_path, chrome_options = options,
			                               desired_capabilities = caps)

	except Exception as e:
		print("Couldn't use the web driver, try to check the version of the driver or the type of browser.")
		raise e
