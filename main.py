from world_meter_scraper import get_data, data_to_dfs, update_main_csvs, data_toCsvs
from db.db_func import continent_data_toDB, country_data_toDB
import time
import schedule


def main():
    '''
    OR: The try is too long. There is no possible to understand where the "crush" can happen.
    maybe:

    try: 
        ** ONE OPERATION, such as: fetch URL **
    except:
        print("Cannot fetch the given url")
    '''
    try:
        start = time.time()

        url = "https://www.worldometers.info/coronavirus"
    	

        '''
        OR: If your functions names make sense, you dont need to write comments. 
        For example: update_main_csvs, is pretty clear what the method do.
        '''
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

def data_to_db():
    '''
    OR: You dont know if the "crush" will be from the import or from the "read_csv"
    '''
    try:
        import pandas as pd
        from paths import allCountries_path, allContinents_path
        countries = pd.read_csv(allCountries_path)
        continents = pd.read_csv(allContinents_path)

    except FileNotFoundError as e:
        raise e

    try:
        country_data_toDB(countries)
        continent_data_toDB(continents)

    except KeyError as e:
        raise(e)

if __name__ == '__main__':
    # data_to_db()

    schedule.every().day.at("22:00").do(main)
    '''
    OR: Great, but maybe there is another way. lets talk about that.
    '''
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait one minute
