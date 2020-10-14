# -*- coding: utf-8 -*-
from prettytable import PrettyTable

from db.db_config import current_db


class DBConnection:
    def __init__(self):
        self.db_engine = current_db.get_engine()
        self.db_engine.connect()


    def read(self, statement):
        """Executes a read query and returns a Prettytable object."""
        data = self.db_engine.execute(statement)
        headers = data.keys()

        data = self.db_engine.execute(statement).fetchall()

        if len(data) == 0:
            return False

        table = PrettyTable(headers)

        for row in data:
            table.add_row(row)

        return table

dbCon = DBConnection()

# TotalCases Min and Max by country.
countries_minMax = dbCon.read('SELECT "Country", "TotalCases" FROM "All countries updated" '
                              'WHERE "TotalCases" IN ((SELECT MAX("TotalCases") FROM "All countries updated"),'
                              '(SELECT MIN("TotalCases") FROM "All countries updated"))')

# TotalCases Min and Max by a continent.
continents_minMax = dbCon.read('SELECT "Continent", "TotalCases" FROM "All continents updated" '
                              'WHERE "TotalCases" IN ((SELECT MAX("TotalCases") FROM "All continents updated" WHERE "Continent" <>  \'World\'),'
                              '(SELECT MIN("TotalCases") FROM "All continents updated")) ')

# Top 15 countries with the highest number of cases.
top15_totalCases = dbCon.read('SELECT "Country","Country_id","Continent_id","TotalCases", RANK() OVER('
                              'ORDER BY "TotalCases" DESC) AS "TotalCases rank","ActiveCases",''"Serious,Critical" FROM "All '
                              'countries ' 'updated" as ''t1 JOIN ''(SELECT "Continent", "Continent_id" FROM "All continents updated") as t2 '
                             'USING("Continent_id") LIMIT 15')

# Countries that are located in Oceania continent.
oceania_countries = dbCon.read('SELECT "Country" FROM "All countries updated" WHERE "Continent_id" = 6')

# The count of countries in each continent.
countries_perContinent = dbCon.read('SELECT "Continent", "Countries count" '
                                    'FROM (SELECT "Continent_id",COUNT(*) as "Countries count" FROM "All countries updated" GROUP BY "Continent_id") AS t1 '
                                    'JOIN (SELECT "Continent", "Continent_id"FROM "All Continents") AS t2 USING("Continent_id") ORDER BY "Countries count" DESC')

# The country with the highest "TotalCases" in each continent.
country_high_perContinent = dbCon.read('SELECT "Country","Continent","maxCases" FROM (SELECT "Continent_id",'
                                       '"Continent" FROM "All Continents") AS t1 JOIN (SELECT "Country",'
                                       '"Continent_id", "TotalCases" AS "maxCases"  FROM "All countries updated" WHERE "TotalCases" IN '
                                       '(SELECT  MAX("TotalCases")  FROM "All countries updated" GROUP BY "Continent_id")) AS t2 '
                                       'USING("Continent_id") ORDER BY "maxCases" DESC')


print(countries_minMax)
print(continents_minMax)
print(top15_totalCases)
print(oceania_countries)
print(countries_perContinent)
print(country_high_perContinent)