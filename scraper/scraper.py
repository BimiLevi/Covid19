from datetime import date, datetime, timedelta
import datetime
import pandas as pd

from resources.paths import create_paths
from scraper.process_func import *
from utilities.directories import create_directory


def run_scraper(yesterday = False):
    counter = 1
    while counter <= 3:
        try:
            html = get_html()
            soup = html_parser(html)
            update_time = latest_update(soup, yesterday = yesterday)
            table = get_table(soup, yesterday = yesterday)
            data = process_table(table)
            break

        except IndexError as ie:
            counter += 1
            print('Unable to process the data due to IndexError.')
            print("The error that occurred is:\n{}\n".format(ie))

            # Three tries before continuing.
            print('The process will start again in 30 seconds.\n This is the {} attempt out of 3.\n'.format(str(
                    counter)))
            time.sleep(30)

    return data, update_time

def data_to_dfs(data, update_time, yesterday = False):
    df = pd.DataFrame.from_dict(data)

    scrap_timestamp = datetime.now().date()
    if yesterday:
        date = scrap_timestamp - timedelta(days = 1)

    else:
        date = scrap_timestamp

    df['Date'] = date.strftime('%Y-%m-%d')
    df['Scrap_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['Update_time_GMT'] = update_time

    try:
        drop_cols = ['1 Caseevery X ppl', '1 Deathevery X ppl', '1 Testevery X ppl']
        df = df.drop(columns = drop_cols)

    except FileNotFoundError as e:
        print('The columns you asked for where not found.'
              'The requested columns are:\n{]'.format(drop_cols))
        print("The error that occurred is:\n{}".format(e))


    continent_df = create_continent_df(df)
    country_df = create_country_df(df)

    """ Calculating the differences between measures by dates"""
    from scraper.calculations import make_calc

    for country in country_df['Country'].tolist():
        row = country_df[country_df['Country'] == country]
        idx = row.index.values

        processed_row = make_calc(row, country)
        country_df.iloc[idx] = processed_row


    for continent in continent_df['Continent'].tolist():
        row = continent_df[continent_df['Continent'] == continent]
        i = row.index.values

        processed_row = make_calc(row, continent)
        continent_df.iloc[i] = processed_row


    return continent_df, country_df

def data_to_csvs(countries, continents, yesterday = False):
    dir_paths = create_paths(yesterday)

    for path in dir_paths:
        create_directory(path)

    dateDay_path = dir_paths[3]

    # Saving the data onto a CSV file.
    print('Saving the data to a CSV file.')

    if yesterday:
        date = (datetime.now() - timedelta(days = 1)).date().strftime("%Y-%m-%d")

    else:
        date = datetime.today().strftime("%Y-%m-%d")

    files_list = [dateDay_path + '/' + 'Countries {}.csv'.format(str(date)),
                  dateDay_path + '/' + 'Continents {}.csv'.format(str(date))]

    countries.to_csv(files_list[0], index=False)
    print('Countries {} csv was successfully created.'.format(str(date)))

    continents.to_csv(files_list[1], index=False)
    print('Continents {} csv was successfully created.'.format(str(date)))


