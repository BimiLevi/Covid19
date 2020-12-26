import schedule

from database.db_config import current_db as db
from resources.tables_func import *
from scraper.scraper import *
from utilities.files_function import calculate_time

def schedule_run(time):
    """ Complexity time O(minute^n)
        Checks every minute if the current time is equal the function 'time' input.
        Time is by the 24-hour clock: hh:mm:ss """

    if type(time) is int:
        time = str(time)

    schedule.every().day.at(time).do(main)
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait one minute

@calculate_time
def main():
    try:

        if not db.table_exists('Countries'):
            print('Creating Countries main table.')
            countries_table(db.get_engine())

        else:
            pass

        if not db.table_exists('Continents'):
            print('Creating Continents main table.')
            continents_table(db.get_engine())

        else:
            pass

    except Exception as e:
        print('Cannot creat the base tables.')
        print("The error that occurred is:\n{}".format(e))

    try:
        # Getting the data out of the website, inserting the data into a dict and returns the dict.
        data, update_time = run_scraper()

    except Exception as e:
        print('Cannot fetch the data from the website.')
        print("The error that occurred is:\n{}".format(e))

    try:
        # Crating a panda's object out of the data, and manipulating it. returns two dataframes.
        continents, countries = data_to_dfs(data, update_time)
        print('The data was inserted into pandas DF successfully.')

    except Exception as e:
        print("Couldn't convert the data into pandas df object.")
        print("The error that occurred is:\n{}".format(e))

    try:
        # Creates csv from the newly scraped data, and saves it by date inside the project directory.
        data_to_csvs(countries, continents)

    except Exception as e:
        print("An error has occurred when trying to save the data to csv's")
        print("The error that occurred is:\n{}".format(e))

    try:
        #  Writing the data into azure PostgresSQL DB.
        df_dict = {'Country': countries, 'Continent': continents}
        for col in df_dict.keys():
            db.df_to_db(col, df_dict[col])

    except Exception as e:
        print("Couldn't write the data onto the DB.")
        print("The error that occurred is:\n{}".format(e))

    # Creating a table for countries and continents that contain only the latest data.
    try:
        continents.to_sql('All continents updated', con = db.get_engine(), if_exists = 'replace', index = False)
        print('"All continents updated" table was successfully created.')

        countries.to_sql('All countries updated', con = db.get_engine(), if_exists = 'replace', index = False)
        print('"All countries updated" table was successfully created.')

    except Exception as e:
        print("Couldn't write the data onto the DB.")
        print("The error that occurred is:\n{}".format(e))

    try:
        db.tables_to_csv()
        print('Tables have been updated locally.')


    except Exception as e:
        print("Unable to updated the data tables locally.")
        print("The error that occurred is:\n{}".format(e))

if __name__ == '__main__':
    # db.restart()
    # schedule_run('23:00')

    main()


