from scraper.world_meter_scraper import get_data, data_to_dfs, data_to_csvs
from db.db_func import load_backup, df_to_db, table_exists
from resources.tables_func import *
from db.engine import engine
import time

def main():
    start = time.time()

    try:

        if not table_exists('Countries'):
            print('Creating Countries main table')
            countries_table()

        else:
            pass

        if not table_exists('Continents'):
            print('Creating Continents main table')
            continents_table()

        else:
            pass

    except Exception as e:
        print('Cannot creat the base tables.')
        print("The error that occurred is:\n{}".format(e))

    try:
        from resources.paths import site_url
        url = site_url

        # Getting the data out of the website, inserting the data into a dict and returns the dict.
        data = get_data(url)

    except Exception as e:
        print('Cannot fetch the data from the website.')
        print("The error that occurred is:\n{}".format(e))

    try:
        # Crating a panda's object out of the data, and manipulating it. returns two dataframes.
        continents, countries = data_to_dfs(data)

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
            df_to_db(col, df_dict[col])

    except Exception as e:
        print("Couldn't write the data onto the DB.")
        print("The error that occurred is:\n{}".format(e))

    # Creating a table for countries and continents that contain only the latest data.
    try:
        continents.to_sql('Latest Update Continents', con = engine, if_exists = 'replace', index = False)
        print('Latest Update Continents table was successfully created.')

        countries.to_sql('Latest Update Countries', con = engine, if_exists = 'replace', index = False)
        print('Latest Update Countries table was successfully created.')

    except Exception as e:
        print("Couldn't write the data onto the DB.")
        print("The error that occurred is:\n{}".format(e))


    end = time.time()
    execution_time = (end - start) / 60
    print('The process executed successfully,the time it took is: {:.3f} minutes.'.format(execution_time))


if __name__ == '__main__':
    # load_backup()

    main()

    import schedule
    # schedule.every().day.at("22:00").do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # Wait one minute


