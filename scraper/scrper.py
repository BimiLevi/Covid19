import re
import time
from datetime import datetime

import requests as req
from bs4 import BeautifulSoup
from tqdm import tqdm

from resources.paths import continents_path
from resources.paths import site_url
from utilities.files_function import load_json


class Scraper:
	def __init__(self, url):

		print('Getting html page.')
		self.html = Scraper.get_html(url)
		print('Html page retrieved.\n')

		self.soup = Scraper.html_parser(self.html)
		self.table = self.get_table()
		# self.data =

	def __str__(self):
		return "The url is: {}\nThe date table is:\n {}".format(self.url, self.table)
	
	@staticmethod
	def get_date_parm():
		year = datetime.now().strftime("%Y")
		month = datetime.now().strftime("%B")
		day = datetime.now().strftime("%d")
		return day, month, year
	
	@staticmethod
	def get_html(url):
		try:
			html_page = req.get(url)

			return html_page

		except req.exceptions.RequestException as e:
			print('Unable to get html page.')
			print("The error that occurred is:\n{}\n".format(e))

	@staticmethod
	def html_parser(html_page):
		try:
			soup = BeautifulSoup(html_page.content, 'html5lib')
			return soup

		except Exception as e:
			print('Unable to parse the html page.')
			print("The error that occurred is:\n{}\n".format(e))

		except req.exceptions.RequestException as e:
			print('Unable to get html page.')
			print("The error that occurred is:\n{}\n".format(e))

	def get_table(self):
		print('Finding the table with the data.')
		table = self.soup.find('table')
		print('Table found.\n')
		return table

	def latest_update(self):
		last_updated = self.soup.find("div", text = re.compile('Last updated')).text.strip().split(" ")
		month = last_updated[2]
		day = last_updated[3].replace(',', '')
		year = last_updated[4].replace(',', '')

		s = year + ' ' + month + ' ' + day

		date = datetime.strptime(s, "%Y %B %d").date()
		time = last_updated[5]

		return date, time

	def process_table(self):
		print('Starting to process the data from the table.')

		def get_headers_list(table_headers):
			header_list = []
			for header in table_headers:
				header_list.append(header.get_text())
			return header_list

		headers_list = get_headers_list(self.table.find('tr').findAll('th'))
		rows = self.table.findAll('tr')

		# Iterating the data, and creating df.
		records = []
		total_data = 0
		with tqdm(total = len(rows), desc = 'Processing the data') as pbar:
			for idy, row in enumerate(rows):
				time.sleep(0.02)
				pbar.update(1)

				cols = row.findAll('td')
				record = {}

				for idx, col in enumerate(cols):
					col_text = col.text.strip()
					if (col_text == 'N/A') or (col_text == ''):  # Filing missing values in the data with None
						record[headers_list[idx]] = None

					else:
						if ',' in col_text:
							col_text = col_text.replace(',', '')

						if '+' in col_text:
							col_text = col_text.replace('+', '')
						record[headers_list[idx]] = col_text

				total_data += 1
				records.append(record)

		print('The data was extracted from the table.\n')
		return records

	def creat_continent_df(self, df):
		try:
			possible_continents = load_json(continents_path)

		except Exception as e:
			print("Unable to load continents json file.")
			print("The error that occurred is:\n{}".format(e))

		try:
			continents_list = possible_continents.keys()
			continent_df = df[df['Country,Other'].isin(continents_list)]

		except KeyError as e:
			raise e

		except Exception as e:
			print("Unable to retrieve the continents from the data.")
			print("The error that occurred is:\n{}".format(e))

		try:
			continent_df = continent_df.drop(columns = ['#', 'TotalTests', 'Population', 'Continent', 'Deaths/1M pop'],
			                                 axis = 1)
		except Exception as e:
			print("Couldn't drop the requested columns from the df.")
			print("The error that occurred is:\n{}".format(e))

		try:
			continent_df = continent_df.rename(columns = {'Country,Other': 'Continent'})
			# Giving each continent a uniq id parm.
			continent_df['Continent_id'] = continent_df['Continent'].map(possible_continents)

		except KeyError as e:
			print("The error that occurred is:\n{}".format(e))

		except Exception as e:
			print("Unable to map continents ID's / rename DF columns.")
			print("The error that occurred is:\n{}".format(e))

		try:
			col_list = ['scrap_date', 'scrap_time', 'update date', 'update time-GMT', 'Continent_id', 'Continent',
			            'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered',
			            'NewRecovered', 'ActiveCases', 'Serious,Critical']

			continent_df = continent_df.reindex(columns = col_list)

		except Exception as e:
			print("Couldn't rename columns names.")
			print("The error that occurred is:\n{}".format(e))

		return continent_df


if __name__ == '__main__':
    from resources.paths import site_url

scraper = Scraper(site_url)
date,time = scraper.latest_update()
print(date,time)