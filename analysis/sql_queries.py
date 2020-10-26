# -*- coding: utf-8 -*-
from prettytable import PrettyTable

from database.db_config import current_db as db


class DBConnection:
    def __init__(self):
        self.db_engine = db.get_engine()
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

# Top 5 countries with active cases.
top5_countries_active = dbCon.read('SELECT "Country","ActiveCases" FROM "All countries updated" WHERE "ActiveCases" '
                                   'IS NOT NULL ORDER BY "ActiveCases" DESC LIMIT 5;')

# The date that israel had the highest value of new cases.
israel_newCases_date = dbCon.read('SELECT "update date" as "max new cases date" FROM "Israel" WHERE "NewCases" = (Select MAX("NewCases") FROM "Israel" )')

# Ranking each continent by its active cases.
continent_active_rank = dbCon.read('SELECT "Country","Continent_id","TotalCases","ActiveCases",RANK() OVER (PARTITION BY "Continent_id" ORDER BY "ActiveCases" DESC) AS "Ranking_inContinent" FROM "All countries updated"')
israel_minMax_dates = dbCon.read('SELECT MIN("update date") as "Earliest Date",MAX("update date") as "Latest Date" '
                                 'FROM "Israel"')

print(countries_minMax)
print(continents_minMax)
print(top15_totalCases)
print(oceania_countries)
print(countries_perContinent)
print(country_high_perContinent)
print(top5_countries_active)
print(israel_newCases_date)
print(continent_active_rank)
print(israel_minMax_dates)