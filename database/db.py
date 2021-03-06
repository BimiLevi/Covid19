# -*- coding: utf-8 -*-
from glob import glob

import numpy as np
import psycopg2
from prettytable import PrettyTable
from sqlalchemy import create_engine, MetaData
import contextlib
from resources.paths import *
from resources.tables_func import *
from utilities.files_function import calculate_time


class Db:
	def __init__(self, username, password, dbname, host, port = 5432):
		self.username = username
		self.password = password
		self.dbname = dbname
		self.host = host
		self.port = port

		self.url = self.create_url()
		self.engine = self.create_engine()

	def __str__(self):
		return '''
username: {}
password: {}
db name: {}
host/server: {}
port: {}
url: {}'''.format(self.username, self.password, self.dbname, self.host, self.port, self.url)

	def create_url(self):
		url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.username, self.password, self.host, self.port,
															self.dbname)
		return url

	def set_port(self, port):
		self.port = port

	def create_engine(self):
		engine = create_engine(self.url, encoding = 'utf-8')
		return engine

	def set_url(self, url):
		self.url = url
		print('Dont forget to creat new engine with the url.')

	def set_engine(self):
		self.engine = self.create_engine()

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
				if table == 'usa':
					table = 'USA'

				elif (table == 'uk') or (table=='Uk'):
					table = 'UK'

				elif (table == "UAE") or (table == "Uae") or (table == 'uae'):
					table = 'UAE'


				elif len(table.split()) == 2:
					word1 = table.split()[0].capitalize()
					word2 = table.split()[1].capitalize()

					table = word1 + ' ' + word2


				elif not table[0].isupper():
					table = table.capitalize()

				if self.table_exists(table):
					table = pd.read_sql(table, con = self.engine)
					table = table.fillna(-1)

					"""Changing columns types"""
					for col in table.columns.tolist():
						table[col] = table[col].astype(general_parm[col], errors = 'ignore')

					table = table.replace(-1, np.nan)

					return table

				else:
					print("The table that you requested doesn't exists in the DB.\n table: {}.".format(table))
					return None

			else:
				return 'The input must be of str type.'

		except psycopg2.Error as e:
			print("The error that occurred is:\n{}".format(e))
			raise ValueError("Unable to connect to DB.")

	def df_to_db(self, col, df, calc = False):
		try:
			dtype_parm = None
			if col == 'Country':
				dtype_parm = countries_parm

			elif col == 'Continent':
				dtype_parm = continents_parm

			headers_list = df[col].drop_duplicates().tolist()

			if not calc:
				"""This part is used when loading the prepared data that was scraped."""
				for header in headers_list:
					temp_df = df[df[col] == '{}'.format(header)]
					temp_df.to_sql('{}'.format(header), con = self.engine, if_exists = 'append', index = False,
								   dtype = dtype_parm)

				print('{} DB was successfully Updated.'.format(col))

			else:
				"""Making calculations before loading the data to db - used when loading data from backup"""
				pd.options.mode.chained_assignment = None  # default='warn'

				for header in headers_list:
					temp_df = df[df[col] == '{}'.format(header)]

					temp_df['NewCases'] = temp_df['TotalCases'].diff()
					temp_df['NewDeaths'] = temp_df['TotalDeaths'].diff()
					temp_df['NewRecovered'] = temp_df['TotalRecovered'].diff()

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
		df = df[df['Date'].max() == df['Date']]
		df = df.sort_values(by = ['TotalCases'], ascending = False)
		return df

	@calculate_time
	def load_backup(self):
		import os
		try:
			print('Creating Countries main table.')
			countries_table(self.engine)

			print('Creating Continents main table.')
			continents_table(self.engine)

			# Complexity time O(n^3)
			ext_list = ["*Countries*", '*Continents*']
			for ext in ext_list:
				all_csv_files = []
				for path, subdir, files in os.walk(Ddate_path):
					for csv_path in glob(os.path.join(path, ext)):
						df = pd.read_csv(csv_path, index_col = None, header = 0)
						all_csv_files.append(df)

				frame = pd.concat(all_csv_files, axis = 0, ignore_index = True)
				frame = frame.sort_values('Date')

				if ext == "*Countries*":
					self.df_to_db('Country', frame, calc = True)
					late_data = self.get_latest_data(frame)
					late_data.to_sql('All countries updated', con = self.engine, if_exists = 'replace', index = False,
									 dtype = countries_parm)

				elif ext == '*Continents*':
					self.df_to_db('Continent', frame, calc = True)
					late_data = self.get_latest_data(frame)
					late_data.to_sql('All continents updated', con = self.engine, if_exists = 'replace', index = False,
									 dtype = continents_parm)

		except Exception as e:
			print('The following Exception as occurred:\n{}'.format(e))

	def tables_to_csv(self):
		tables_list = self.get_tables_names()
		for table in tables_list:
			path = Dtables_path + r'\{}.csv'.format(table)

			temp_table = self.get_table(table)
			if not temp_table is None:
				temp_table.to_csv(path, index = False)

			else:
				pass

	def sql_query(self, statement):
		"""Executes a read query and returns a Prettytable object."""
		self.engine.connect()

		res = self.engine.execute(statement)
		headers = res.keys()
		data = res.fetchall()

		if len(data) == 0:
			return False

		table = PrettyTable(headers)

		for row in data:
			table.add_row(row)

		return table

	def execute_ddl(self, statement):
		try:
			self.engine.execute(statement)
			print('DDL executed successfully.')

		except Exception as e:
			print(f'The following exception has occurred:\n{e}')

	def drop_schema(self):
		print('Dropping all tables')
		con = self.engine.connect()
		con.execute('DROP SCHEMA public CASCADE;'
					'CREATE SCHEMA public;')

	def restart(self, tablesCsv = False):
		""" Complexity Time O(n).
			Drop all the tables in db, and creates new public schema, using SQL query.
				Afterwards loading the data back for csv file in the Data directory. """
		try:
			self.drop_schema()

			print('Loading all of the data to DB')
			self.load_backup()

			if tablesCsv:
				self.tables_to_csv()
				print("Tables csv files generated")

		except Exception as e:
			print(f'Unable to complete the restart\nThe following Error occurred\n{e}')

