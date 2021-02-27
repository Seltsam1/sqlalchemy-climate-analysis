# Climate app

# Dependencies
from flask import Flask, jsonify

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Route for json dictionary of data
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

    # precipitation_dict = [u.__dict__ for u in session.query(Measurement.date, Measurement.prcp).\
    #    filter(func.strftime(Measurement.date >= year_date)).all()]

    for date, prcp in date_results:
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp



    # JSON dctionary of results
    return jsonify(precipitation_dict)




        




if __name__ == "__main__":
    app.run(debug=True)
