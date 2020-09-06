import pandas as pd
import glob
from Utilities.files_function import load_json

country_path = r'C:\Users\talle\PycharmProjects\Covid19\Utilities\countries id'
continent_path = r'C:\Users\talle\PycharmProjects\covid19\Utilities\continent id'

possible_continents = load_json(continent_path)
possible_countries = load_json(country_path)

# continent_df['Continent_id'] = continent_df['Continent'].map(possible_continents)

path = r'C:\Users\talle\PycharmProjects\Covid19\old_scripts\continentAll'
all_files = glob.glob(path + "/*.csv")

li = []

# for filename in all_files:
#     df = pd.read_csv(filename, index_col=None, header=0)
#     li.append(df)
#
# continents_df = pd.concat(li, axis=0, ignore_index=True)
# continents_df = continents_df.drop(columns = ['Unnamed: 0'])
# continents_df['Continent_id'] = continents_df['Continent'].map(possib le_continents)
# continents_df.to_csv('all_continents.csv', index=False)

from DB.db_func import continent_data_toDB
df = pd.read_csv(r'C:\Users\talle\PycharmProjects\Covid19\old_scripts\all_continents.csv')
continent_data_toDB(df)
