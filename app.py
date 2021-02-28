# Climate app

# Dependencies
from flask import Flask, jsonify

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

import numpy as np


#################################################
# Database Setup
#################################################

database_path = "./Resources/hawaii.sqlite"

engine = create_engine(f"sqlite:///{database_path}")

Base = automap_base()

Base.prepare(engine, reflect=True)

# References to tables
Measurement = Base.classes.measurement
Station = Base.classes.measurement


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Route for homepage
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Climate API!<br/>"
        f"<p></p>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        f"<p></p>"
        f"Note - manually enter desired dates for 'start' and 'end' points of routes in format yyyy-mm-dd"
    )

# Route for json dictionary of precipitation data for past year
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Start session with database
    session = Session(engine)

    # Query past year of precipitation data
    year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    date_results = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime(Measurement.date >= year_date)).all()

    # Close session
    session.close()

    # Create dictionary
    precipitation_dict = {}
    precipitation_dict = dict(date_results)

    # JSON dctionary of results
    return jsonify(precipitation_dict)


# Route for json list of stations
@app.route("/api/v1.0/stations")
def stations():

    # Start session with database
    session = Session(engine)

    # Query stations
    station_list = session.query(Station.station).\
        group_by(Station.station).all()

    # Close session
    session.close()

    # Convert list of tuples into a list
    station_list = list(np.ravel(station_list))

    # JSON list of results
    return jsonify(station_list)


# Route for dates and temperature for most active station for past year
@app.route("/api/v1.0/tobs")
def tobs():

    # Start session with database
    session = Session(engine)

    # Query stations
    year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_results = session.query(Measurement.tobs).\
        filter(func.strftime(Measurement.date >= year_date)).\
        filter(Measurement.station == 'USC00519281').all()

    # Close session
    session.close()
    
    # Convert list of tuples into a list
    temp_list = list(np.ravel(temp_results))

    # JSON list of results
    return jsonify(temp_list)


# Routes for minimum, maximum, and average temperate for a given starting date and for a range of dates
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperatue(start=None, end=None):

    # Start session with database
    session = Session(engine)

    # Variable to use in query
    sel = [
       func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)
    ]

    # if statement for start date api route
    if not end:

        # Query
        start_results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        # Close session
        session.close()

        # Convert to list
        start_list = list(np.ravel(start_results))

        # Return print results of query
        return (
            f"For start date {start}:</br>"
            "<p></p>"
            f"The lowest temperature is {start_list[0]}.</br>"
            f"The highest temperture is {start_list[1]}.</br>"
            f"The average temperature is {round((start_list[2]),2)}.</br>"
        )
    # else statement for start and end date api route
    else:

        # Query
        range_results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

        # Close session
        session.close()

        # Convert to list
        range_list = list(np.ravel(range_results))

        # Return print results of query
        return (
            f"For start date {start} and end date {end}:</br>"
            "<p></p>"
            f"The lowest temperature is {range_list[0]}.</br>"
            f"The highest temperture is {range_list[1]}.</br>"
            f"The average temperature is {round((range_list[2]),2)}.</br>"
        )


# To run applicaton

if __name__ == "__main__":
    app.run(debug=True)
