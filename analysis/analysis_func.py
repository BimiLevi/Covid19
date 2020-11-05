import calendar

import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2


def data_by_month(df, month, year):
    if type(month) != int:
        raise TypeError('Month must be of int type.')

    data = df[(df['scrap_date'].dt.month == month) & (df['scrap_date'].dt.year == year)]
    return data.reset_index(drop = True)

def data_range_date(df, startDate, endDate):
    firstDate = df['scrap_date'].min().date()
    lastDate = df['scrap_date'].max().date()

    startDate = pd.to_datetime(startDate).date()
    endDate = pd.to_datetime(endDate).date()

    if (startDate < firstDate) or (endDate > lastDate) or (startDate > endDate):
        raise ValueError('One of the dates surpass boundaries')

    data = df[(str(startDate) <= df['scrap_date']) & (df['scrap_date'] <= str(endDate))].reset_index(drop = True)
    return data

def get_minmax(df, col):
    min_val = df[df[col] == df[col].min()][col]
    max_val = df[df[col] == df[col].max()][col]

    min_max = pd.concat([min_val, max_val])
    return min_max

def get_top(df, col, n=10):

    if (type(n) != int) or (type(col) != str):
        raise TypeError('n = int, col = str')

    elif not isinstance(df, pd.DataFrame):
        raise TypeError('df = dataframe')


    col_list = df.columns.tolist()

    if 'Continent' in col_list:
        if col == 'TotalTests':
            return

        sorted_df = df[['Continent', col]].sort_values(col, ascending = False)
        top = sorted_df.head(n).reset_index(drop = True)
        return top

    elif 'Country' in col_list:
        sorted_df = df[['Country', col]]	.sort_values(col, ascending = False)
        top = sorted_df.head(n).reset_index(drop = True)
        return top

    else:
        return 'Error neither countries or continents were called.'

def first_day_of_month(date):
    day = calendar.weekday(date.year, date.month, 1)
    return calendar.day_name[day]

def get_codes(col):
    try:
        cn_a2_code = country_name_to_country_alpha2(col)
    except:
        cn_a2_code = 'Unknown'
    try:
        cn_continent = country_alpha2_to_continent_code(cn_a2_code)
    except:
        cn_continent = 'Unknown'
    return (cn_a2_code, cn_continent)

geolocator = Nominatim(user_agent="https")
def geolocate(country):
    loc = None

    try:
        loc = geolocator.geocode(country)
        loc = (loc.latitude, loc.longitude)

    except:
        loc = np.nan

    finally:
        return loc


