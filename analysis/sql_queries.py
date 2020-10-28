# -*- coding: utf-8 -*-

from database.db_config import current_db as db


# TotalCases Min and Max by country.
countries_minMax = db.sql_query('SELECT "Country", "TotalCases" FROM "All countries updated" '
                              'WHERE "TotalCases" IN ((SELECT MAX("TotalCases") FROM "All countries updated"),'
                              '(SELECT MIN("TotalCases") FROM "All countries updated"))')

# TotalCases Min and Max by a continent.
continents_minMax = db.sql_query('SELECT "Continent", "TotalCases" FROM "All continents updated" '
                              'WHERE "TotalCases" IN ((SELECT MAX("TotalCases") FROM "All continents updated" WHERE "Continent" <>  \'World\'),'
                              '(SELECT MIN("TotalCases") FROM "All continents updated")) ')

# Top 15 countries with the highest number of cases.
top15_totalCases = db.sql_query('SELECT "Country","Continent","TotalCases",RANK() OVER(PARTITION BY "Continent" ORDER BY "TotalCases" DESC) AS "Continent_rank_by_TotalCases","ActiveCases","SeriousCritical" FROM (SELECT "Country_id","Continent_id" FROM "All Countries") AS t1 JOIN  (SELECT * FROM "All Continents") AS t2 USING("Continent_id") JOIN  (SELECT "Country","Country_id","TotalCases","ActiveCases","SeriousCritical"  FROM "All countries updated" LIMIT 15) AS t3 USING("Country_id")')

# Countries that are located in Oceania continent.
oceania_countries = db.sql_query('SELECT "Country" FROM "All Countries" WHERE "Continent_id" IN (SELECT '
                                 '"Continent_id" FROM "All Continents" WHERE "Continent" = \'Oceania\')')

# The count of countries in each continent.
countries_perContinent = db.sql_query('SELECT "Continent","Countires_count" FROM (SELECT * FROM "All Continents") AS ''t1 JOIN (SELECT "Continent_id", COUNT("Country") AS "Countires_count" FROM "All Countries" GROUP BY "Continent_id") AS t2 USING("Continent_id") ORDER BY "Countires_count" DESC')

# The country with the highest "TotalCases" in each continent.
country_high_perContinent = db.sql_query('SELECT "Country","Continent","TotalCases" FROM (SELECT "Country","Continent","TotalCases" ,RANK() OVER(PARTITION BY "Continent" ORDER BY "TotalCases" DESC) AS "rank" FROM (SELECT "Country","Country_id","TotalCases" FROM "All countries updated" ) AS t1  JOIN (SELECT "Country_id", "Continent_id" FROM "All Countries") AS t2 USING("Country_id")  JOIN (SELECT "Continent_id","Continent" FROM "All Continents") AS t3 USING("Continent_id")) AS t4 WHERE "rank" =1;')

# Top 5 countries with active cases.
top5_countries_active = db.sql_query('SELECT "Country","ActiveCases" FROM "All countries updated" WHERE "ActiveCases" '
                                   'IS NOT NULL ORDER BY "ActiveCases" DESC LIMIT 5;')

# The date that israel had the highest value of new cases.
israel_newCases_date = db.sql_query('SELECT "scrap_date" AS "max_NewCases_date" FROM "Israel" WHERE "NewCases" = (Select MAX("NewCases") FROM "Israel")')

# Ranking each continent by its active cases.
continent_active_rank = db.sql_query('SELECT "Continent","ActiveCases", RANK() OVER(ORDER BY "ActiveCases" DESC) FROM "All continents updated" WHERE "Continent" <> \'World\'')

israel_minMax_dates = db.sql_query('SELECT MIN("scrap_date") as "Earliest Date",MAX("scrap_date") as "Latest Date" FROM "Israel"')

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