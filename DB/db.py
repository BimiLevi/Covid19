# -*- coding: utf-8 -*-
import time
from glob import glob

import psycopg2
from sqlalchemy import create_engine

from db.tables_parm import countries_parm, continents_parm
from resources.paths import world_path
from resources.tables_func import *


class Db:
	def __init__(self, username, password, dbname, host, port = 5432):
		self.username = username
		self.password = password
		self.dbname = dbname
		self.host = host
		self.port = port
		self.url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.username, self.password, self.host, self.port,
		                                                      self.dbname)
		self.engine = self.set_engine(self.url)

	def __str__(self):
		return '''
username: {}
password: {}
db name: {}
host/server: {}
port: {}
url: {}'''.format(self.username, self.password, self.dbname, self.host, self.port, self.url)

	@staticmethod
	def set_engine(url):
		engine = create_engine(url, encoding = 'utf-8')
		return engine

	def get_engine(self):
		return self.engine

	def get_url(self):
		return self.url

	def get_tables_names(self):
		tables_list = []
		with self.engine.connect() as con:
			res = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
			tables = res.fetchall()
			for table in tables:
				tables_list.append(table[0])

		return tables_list

	def table_exists(self, table):
		tables_list = self.get_tables_names()

		if table in tables_list:
			return True

		else:
			return False

	# This func returns pandas object.
	def get_table(self, table):
		try:
			if type(table) == str:
				if not table[0].isupper():
					table = table.capitalize()

				if self.table_exists(table):
					table = pd.read_sql(table, con = self.engine)
					return table

				else:
					return "The table that you requested doesn't exists in the DB."

			else:
				return 'The input must be of str type.'

		except psycopg2.Error as e:
			print("The error that occurred is:\n{}".format(e))
			raise ValueError("Unable to connect to DB.")

	def df_to_db(self, col, df):
		try:
			dtype_parm = None
			if col == 'Country':
				dtype_parm = countries_parm

			elif col == 'Continent':
				dtype_parm = continents_parm

			headers_list = df[col].drop_duplicates().tolist()
			for header in headers_list:
				temp_df = df[df[col] == '{}'.format(header)]
				temp_df.to_sql('{}'.format(header), con = self.engine, if_exists = 'append', index = False,
				               dtype = dtype_parm)

			print('{} DB was successfully Updated.'.format(col))

		except ConnectionError as e:
			print('Unable to connect to DB.')
			raise e

		except Exception as e:
			print("Couldn't dump the data in to DB.")
			print("The error that occurred is:\n{}".format(e))

	@staticmethod
	def get_latest_data(df):
		df = df[df['scrap_date'].max() == df['scrap_date']]
		df = df.sort_values(by = ['TotalCases'], ascending = False)
		return df

	def load_backup(self):
		import os
		try:
			start = time.time()

			print('Creating Countries main table')
			countries_table(self.engine)

			print('Creating Continents main table')
			continents_table(self.engine)

			# Complexity time O(n^3)
			ext_list = ["*Countries*", '*Continents*']
			for ext in ext_list:
				all_csv_files = []
				for path, subdir, files in os.walk(world_path):
					for csv_path in glob(os.path.join(path, ext)):
						df = pd.read_csv(csv_path, index_col = None, header = 0)
						all_csv_files.append(df)

				frame = pd.concat(all_csv_files, axis = 0, ignore_index = True)
				frame = frame.sort_values('scrap_date')

				if ext == "*Countries*":
					self.df_to_db('Country', frame)
					late_data = self.get_latest_data(frame)
					late_data.to_sql('Latest Update Countries', con = self.engine, if_exists = 'replace', index = False,
					                 dtype = countries_parm)

				elif ext == '*Continents*':
					self.df_to_db('Continent', frame)
					late_data = self.get_latest_data(frame)
					late_data.to_sql('Latest Update Continents', con = self.engine, if_exists = 'replace', index = False,
					                 dtype = continents_parm)

			end = time.time()
			execution_time = (end - start) / 60
			print('The process executed successfully,the time it took is: {:.3f} minutes.\n'.format(execution_time))

		except Exception as e:
			print('The following Exception as occurred:\n{}'.format(e))






