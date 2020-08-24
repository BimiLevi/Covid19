from world_meter_scraper import get_data, data_to_dfs, data_toCsvs
from Utilities.db import continent_data_toDB, country_data_toDB

import time
import schedule

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

def main():
    try:
        url = "https://www.worldometers.info/coronavirus"
        data = get_data(url)
        continents, countries = data_to_dfs(data)
        continent_data_toDB(continents), country_data_toDB(countries)
        data_toCsvs(countries, continents)
        print('The process executed successfully, time finished: {}'.format(current_time))

    except:
        print('An Error has occurred.')

if __name__ == '__main__':
    schedule.every().day.at("10:59").do(main)
    schedule.every().day.at("22:59").do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait one minute
