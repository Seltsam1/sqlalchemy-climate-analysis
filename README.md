# sqlalchemy-climate-analysis
Analysis of climate of Hawaii using python

## Getting Started

- Download folder structure
  - Resource folder contains the sqlite file (hawaii.sqlite) used in analyses
  - Jupyter Notebook file (climate_analysis.ipynb) contains preliminary analyses
  - Python file (app.py) contains the "climate api" which can be run from Terminal

## Features

climate_analysis.ipynb
- Uses SQLAlchemy to query the sqlite file
  - Exploratory precipitation analysis involves the last year of data
    - Includes a chart of precipitation by date
  - Exploratory station analysis involves the last year of data for the most active weather station
    - Includes minimum, maximum, and average temperature
    - Includes a histogram of frequency of temperatures

app.py
- Uses Flask to initiate an app instance
  - Lists 5 routes:
    - home route shows path for all available routes
    - precipitation route returns a JSON dictionary of dates and precipitation in inches for the last year of data
    - stations route returns a JSON list of the available station id's in the data
    - tobs route returns a JSON list of temperatures for the past year
    - start route returns print statements of minimum, maximum, and average temperature based on a user specified start date in path
    - start/end route does the same as start route but for a start and end date specified by user in path

## Licensing by:

The code in this project is licensed under MIT license.
