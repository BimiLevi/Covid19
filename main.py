from scraper.world_meter_scraper import get_data, data_to_dfs, data_to_csvs
from db.db_func import load_backup, df_to_db, table_exists
from resources.tables_func import *
import time
import schedule


def main():
    try:
        start = time.time()

        if not table_exists('Countries'):
            print('Creating Countries main table')
            countries_table()

        if not table_exists('Continents'):
            print('Creating Continents main table')
            continents_table()

        from resources.paths import site_url
        url = site_url

        # Getting the data out of the website, inserting the data into a dict and returns the dict.
        data = get_data(url)

        # Crating a panda's object out of the data, and manipulating it. returns two dataframes.
        continents, countries = data_to_dfs(data)

        # Creates csv from the newly scraped data, and saves it by date inside the project directory.
        data_to_csvs(countries, continents)

        #  Writing the data into azure PostgresSQL DB.
        df_dict = {'Country': countries, 'Continent': continents}
        for col in df_dict.keys():
            df_to_db(col, df_dict[col])

        end = time.time()
        execution_time = (end - start) / 60
        print('The process executed successfully,the time it took is: {:.3f} minutes.'.format(execution_time))

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()

    # load_backup()
    #
    # schedule.every().day.at("22:00").do(main)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)  # Wait one minute


