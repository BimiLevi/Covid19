# Covid19 - WorldMeter Web Scraper and Analysis
## Introduction
The goal of this project is to conduct a full ETL process and finally analyzing the gathered data using different analysis technics, visualizations, and implement various ML algorithms.

##  Motivation and Data
Covid 19 pandemic has come to the world attention on Dec. 31, 2019, when authorities alerted the World Health Organization of pneumonia cases in Wuhan City, Hubei province, China. This pandemic has been changing the world since its first outbreak, thousands of countries around the world are trying to fight the virus. Thie virus has a great impact on all our lives, it's effects are felt in numerous different aspects of it such as financially, socially, healthcare, and more.
"World meter" website shows real-time live world statistics, this website that its credibility is fairly high presenting data on Covid19 in 214 countries and territories around the world.

The data that is in use in this project has been scraped out of ["World Meter"](https://www.worldometers.info/coronavirus/) website.

## Project Description:
This project is written in python.
1. **ETL**
- Extraction:
  * Scarping the data from the website HTML page, using requests and Beutifullsoup models.
- Transformation:
  * Cleaning the data.
  * Inserting the data into pandas DF and splitting it to countries and continents.
  * Defining data types for each column.
  * Creation of a unique ID for each country and continent.
  * Removing unwanted columns and header's name change.
  * Mapping Countries to continents. 
- Load:<br/>Dumping the transformed data into Microsoft Azure cloud service PostgreSQL Database, Sqlalchemy is used to establish a connection with the DB.<br/>
The data is loaded for each country and continent, furthermore, an extra four tables are created:
  * "All countries updated" - this table shows the most recent information for each country.
  * "All continents updated" - this table shows the most recent information for each continent.
  * "All Countries" - this table contains the country's names, countries ID's, and the relevant continent ID.
  * "All Continents" - this table contains the continent's names and continents ids. <br/>
  
  The first two tables give a view of the world's situation and the last two tables are used to simplify the connection between continents and countries.
  
  **Database Schema**
![Alt text](https://github.com/BimiLevi/Covid19/blob/master/Covid%2019%20-%20db%20schema.png) 

2. **Analysis**
  * Performing SQL queries.<br/>
     Notebook:https://nbviewer.jupyter.org/github/BimiLevi/Covid19/blob/master/analysis/SQL_queries.ipynb
  * Creating a Jupiter notebook analysis format for countries, including visualizations (Matplotlib, Plotly)
     Notebook:https://nbviewer.jupyter.org/github/BimiLevi/Covid19/blob/master/analysis/country_analysis.ipynb
     ![Alt text](https://github.com/BimiLevi/Covid19/blob/master/analysis/plots/usa/usa%20line%20plot.png)
     ![Alt text](https://github.com/BimiLevi/Covid19/blob/master/analysis/plots/usa/USA%20-%20daily%20increase.png)
     ![Alt text](https://github.com/BimiLevi/Covid19/blob/master/analysis/plots/usa/Usa%20in%20November.svg)
     
 

## Currently under work:
  * Creating continent analysis Jupiter notebook.
  * Preprocessing the data for Ml analysis.
  * Preforming Ml analysis using Scikitlearn.  
  
## Data
**The earliest data is dated to Aug. 02, 2020** (not all days are accounted for in the data). <br/>
The data that is loaded into this repository is of CSV type, and it is separated into two:
  * Daily - for each day there are two CSV's (countries and continents).
  * Table - one CSV for each table that exists in the DB.  





