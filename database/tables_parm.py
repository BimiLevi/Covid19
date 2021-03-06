import sqlalchemy as sa

# Types for PostgresSQL db - dumping.
countries_parm = {'Date': sa.Date(),
                  'Scrap_time': sa.String(),
                  'Update_time_GMT': sa.Time(),
                  'Country_id': sa.Integer(),
                  'Country': sa.String(),
                  'Population': sa.Integer(),
                  'TotalCases': sa.Integer(),
                  'NewCases': sa.Integer(),
                  'TotalDeaths': sa.Integer(),
                  'NewDeaths': sa.Integer(),
                  'TotalRecovered': sa.Integer(),
                  'NewRecovered': sa.Integer(),
                  'ActiveCases': sa.Integer(),
                  'Serious,Critical': sa.Integer(),
                  'Tot_Cases_1M_pop': sa.Integer(),
                  'Deaths/1M pop': sa.Float(),
                  'TotalTests': sa.Integer(),
                  'Tests_1M_pop': sa.Integer(),
                  'Continent_id': sa.Integer()
                  }

continents_parm = {'Date': sa.Date(),
                   'Scrap_time': sa.String(),
                   'Update_time_GMT': sa.Time(),
                   'Continent_id': sa.Integer(),
                   'Continent': sa.String(),
                   'TotalCases': sa.Integer(),
                   'NewCases': sa.Integer(),
                   'TotalDeaths': sa.Integer(),
                   'NewDeaths': sa.Integer(),
                   'TotalRecovered': sa.Integer(),
                   'NewRecovered': sa.Integer(),
                   'ActiveCases': sa.Integer(),
                   'Serious,Critical': sa.Integer()
                   }

# For loading the table from the DB to pandas DF.
general_parm = {'Date': 'datetime64[ns]',
                'Scrap_time': 'object',
                'Update date': 'datetime64[ns]',
                'Update_time_GMT': 'datetime64[ns]',
                'Country_id': 'int64',
                'Country': 'object',
                'Population': 'int64',
                'TotalCases': 'int64',
                'NewCases': 'int64',
                'TotalDeaths': 'int64',
                'NewDeaths': 'int64',
                'TotalRecovered': 'int64',
                'NewRecovered': 'int64',
                'ActiveCases': 'int64',
                'SeriousCritical': 'int64',
                'Tot_Cases_1Mpop': 'int64',
                'Deaths_1Mpop': 'float64',
                'TotalTests': 'int64',
                'Tests_1Mpop': 'int64',
                'Continent_id': 'int64',
                'Continent': 'object'}

