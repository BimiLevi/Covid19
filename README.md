# Covid19 - WorldMeter Web Scraper and Analysis
## Introduction
The goal of this project is to conduct a full ETL process and finally analyzing the gathered data using different analysis technics, visualizations, and implement various ML algorithms.

##  Motivation and Data
Covid 19 pandemic has come to the world attention on Dec. 31, 2019, when authorities alerted the World Health Organization of pneumonia cases in Wuhan City, Hubei province, China. This pandemic has been changing the world since its first outbreak, thousands of countries around the world are trying to fight the virus. Thie virus has a great impact on all our lives, it's effects are felt in numerous different aspects of it such as financially, socially, healthcare, and more.
"World meter" website shows real-time live world statistics, this website that its credibility is fairly high presenting data on Covid19 in 214 countries and territories around the world.

The data that is in use in this project has been scraped out of ["World Meter"](https://www.worldometers.info/coronavirus/) website.

## Project Description:
This project is written in python. 
1. ETL - Complete
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

2. Analysis - Under work
  * Performing SQL queries.

## Currently under work:
  * Data visualization using Matplotlib and Tableau.
  * Preprocessing the data for Ml analysis.
  * Preforming Ml analysis using Scikitlearn.  
  
## Database Schema
![Alt text](https://github.com/BimiLevi/Covid19/blob/master/Covid%2019%20-%20%20Database%20schema.png) 


