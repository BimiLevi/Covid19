import matplotlib.pyplot as plt
import pandas as pd

from analysis.classes import Country

pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 5)

country = Country('USA')
df = country.data  # Pandas df object, that contains the data from the db.

"Understanding the basics of the data."

print("Part 1: Intro")
print(country)
# print(df.head)
print(df.dtypes)
# print(df.isnull().sum())
print('---------------------------------------------------------------------------------------------------------------')
print("Part 2: Basic exploring")

print("Q1. Find the date of the day with the highest New Cases.")
date = df[df['NewCases'] == df['NewCases'].max()]['scrap_date'].dt.date
print('Answer:\n', date)

print("Q2. Find the countries daily increases in death,recoveries,active cases")
death_rate = df['NewDeaths'].pct_change()
country.daily_increase('NewDeaths',save = True)

recovered_rate = df['NewRecovered'].pct_change()
country.daily_increase('NewRecovered',save = True)

newcase_rate = df['NewCases'].pct_change()
country.daily_increase('NewCases',save = True)

print("Q3. ")

plt.show()


