from scraper.world_meter_scraper import get_data, data_to_dfs, data_to_csvs
from db.db_func import load_backup, df_to_db, table_exists
from resources.tables_func import *
import time
import schedule

def main():
    start = time.time()

    try:

        if not table_exists('Countries'):
            print('Creating Countries main table')
            countries_table()

        if not table_exists('Continents'):
            print('Creating Continents main table')
            continents_table()

    except Exception as e:
        print('Cannot creat the base tables.')
        raise e

    try:
        from resources.paths import site_url
        url = site_url

        data = get_data(url)

    except Exception as e:
        print('Cannot fetch the data from the website.')
        raise e

    try:
        continents, countries = data_to_dfs(data)

    except Exception as e:
        print("Couldn't convert the data into pandas df object.")
        raise e

    try:
        data_to_csvs(countries, continents)

    except Exception as e:
        print("An error has occurred when trying to save the data to csv's")
        raise e

    try:
        df_dict = {'Country': countries, 'Continent': continents}

        #  Writing the data into azure PostgresSQL DB.
        for col in df_dict.keys():
            df_to_db(col, df_dict[col])

    except Exception as e:
        print("Couldn't writ the data onto the DB.")
        raise e

    end = time.time()
    execution_time = (end - start) / 60
    print('The process executed successfully,the time it took is: {:.3f} minutes.'.format(execution_time))


if __name__ == '__main__':
    pass
    # load_backup()
    schedule.every().day.at("22:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait one minute


