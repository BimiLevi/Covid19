import pandas as pd
import glob
from Utilities.files_function import load_json

country_path = r'C:\Users\talle\PycharmProjects\Covid19\Utilities\countries id'
continent_path = r'C:\Users\talle\PycharmProjects\covid19\Utilities\continent id'

possible_continents = load_json(continent_path)
possible_countries = load_json(country_path)

# continent_df['Continent_id'] = continent_df['Continent'].map(possible_continents)

path = r'C:\Users\talle\PycharmProjects\Covid19\old_scripts\countriesAll'
all_files = glob.glob(path + "/*.csv")

li = []

# for filename in all_files:
#     df = pd.read_csv(filename, index_col=None, header=0)
#     li.append(df)
# 
# country_df = pd.concat(li, axis=0, ignore_index=True)
# country_df = country_df.drop(columns = ['Unnamed: 0'])
# country_df['Country_id'] = country_df['Country'].map(possible_countries)
# country_df['Continent_id'] = country_df['Continent'].map(possible_continents)

# desired_cols = country_df.iloc[:, 1:].drop(columns = ['Population']).columns.tolist()
# col_titles = ['Country_id', 'Country', 'Population'] + desired_cols
# country_df = country_df.reindex(columns = col_titles)
# 
# country_df.to_csv('all_countries.csv')
# df = pd.read_csv('all_countries.csv')

# country_df.to_csv('all_countries.csv', index=False)

from DB.db_func import country_data_toDB
country_data_toDB(pd.read_csv(r'C:\Users\talle\PycharmProjects\Covid19\old_scripts\all_countries.csv'))

