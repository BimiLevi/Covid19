from world_meter_scraper import get_data, data_to_dfs, update_main_csvs, data_toCsvs
from DB.db_func import continent_data_toDB, country_data_toDB
import time
import timeit
import schedule


def main():
    try:
        start = time.time()

        url = "https://www.worldometers.info/coronavirus"

        # Getting the data out of the website, inserting the data into a dict and returns the dict.
        data = get_data(url)

        # Crating a panda's object out of the data, and manipulating it. returns two dataframes.
        continents, countries = data_to_dfs(data)

        # Updating the two main csv that contain the entire data.
        update_main_csvs(countries, continents)

        # Creates csv from the newly scraped data, and saves it by date inside the project directory.
        data_toCsvs(countries, continents)

        # Writing the data into azure PostgresSQL DB.
        # Countries df is written for each country separately!
        continent_data_toDB(continents)

        # Continents df is written for each continent separately!
        country_data_toDB(countries)

        end = time.time()
        execution_time = (end - start) / 60
        print('The process executed successfully,the time it took is: {:.3f} minutes.'.format(execution_time))

    except:
        print('An Error has occurred.')

if __name__ == '__main__':
    schedule.every().day.at("22:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait one minute
