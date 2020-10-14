# -*- coding: utf-8 -*-
from db.db_config import current_db

class DBConnection:
    def __init__(self):
        self.db_engine = current_db.get_engine()
        self.db_engine.connect()

    def read(self, statement):
        """Executes a read query and returns a list of dicts, whose keys are column names."""
        data = self.db_engine.execute(statement).fetchall()
        results = []

        if len(data) == 0:
            return results

        # results from sqlalchemy are returned as a list of tuples; this procedure converts it into a list of dicts
        for row_number, row in enumerate(data):
            results.append({})
            for column_number, value in enumerate(row):
                results[row_number][row.keys()[column_number]] = value

        return results

dbCon = DBConnection()


countries_minMax = dbCon.read('SELECT "Country", "TotalCases" FROM "Latest Update Countries" '
                              'WHERE "TotalCases" IN ((SELECT MAX("TotalCases") FROM "Latest Update Countries"),'
                              '(SELECT MIN("TotalCases") FROM "Latest Update Countries"))')

continents_minMax = dbCon.read('SELECT "Continent", "TotalCases" FROM "Latest Update Continents" '
                              'WHERE "TotalCases" IN ((SELECT MAX("TotalCases") FROM "Latest Update Continents" WHERE "Continent" <>  \'World\'),'
                              '(SELECT MIN("TotalCases") FROM "Latest Update Continents")) ')

top15_totalCases = dbCon.read('SELECT "Country","Country_id","Continent","Continent_id","TotalCases","ActiveCases",'
                             '"Serious,Critical" FROM "Latest Update Countries" as t1 JOIN '
                             '(SELECT "Continent", "Continent_id" FROM "Latest Update Continents") as t2 '
                             'USING("Continent_id") ORDER BY "TotalCases" DESC LIMIT 15')

oceania_countries = dbCon.read()

