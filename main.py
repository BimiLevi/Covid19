from world_meter_scraper import get_data, data_to_dfs, data_toCsvs
from DB.db_func import continent_data_toDB, country_data_toDB
import time
import timeit
import schedule


def main():
    try:
        start = time.time()

        url = "https://www.worldometers.info/coronavirus"
        data = get_data(url)
        continents, countries = data_to_dfs(data)
        data_toCsvs(countries, continents)
        continent_data_toDB(continents), country_data_toDB(countries)

        end = time.time()
        execution_time = (end - start)
        print('The process executed successfully,the time it took is: {:.3f} seconds.'.format(execution_time))

    except:
        print('An Error has occurred.')

if __name__ == '__main__':
    schedule.every().day.at("23:30").do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait one minute
