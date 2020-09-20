# import pandas as pd
#
# try:
#     df = pd.read_csv(r'C:\Users\talle\PycharmProjects\Covid19\main csvs\main_countries.csv',error_bad_lines=False,warn_bad_lines=False,delimiter=',')
#     cols_list = ['Population', 'TotalCases', 'TotalCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered','ActiveCases','Serious,Critical','Tot/Cases/1M pop','Deaths/1M pop','TotalTests','Tests_1M_pop']
#
#     for col in cols_list:
#         df[col] = df[col].str.replace(',', '')
#
#     df.to_csv(r'C:\Users\talle\PycharmProjects\Covid19\main csvs\main_countries1.csv')
#
# except Exception as e:
#     raise (e)
#


def trailing_zeros(row):
    comma = ','

    if not comma in row:
        return row

    else:
        count = row.count(comma)
        new_raw = row.repalce(',', '')

        if count == 1:
            if len(new_raw) == 2:
                new_raw = int(new_raw) * 100
                return new_raw

            elif (len(new_raw) == 3) or (len(new_raw) == 4) or (len(new_raw) == 5):
                new_raw = int(new_raw) * 10

                return new_raw
        else:
            return new_raw

