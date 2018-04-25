import datetime as dt
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

today=str(date.today())
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite",echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement=Base.classes.measurements
Station=Base.classes.stations
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and precipitation observations from the last year."""
    rain=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=(dt.datetime.today() - relativedelta(years=1))).all()

    # Convert list of tuples into dictionary
    prcp = dict(rain)

    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    # Query all passengers
    stations=session.query(Station.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    # Query all passengers
    temps=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=(dt.datetime.today() - relativedelta(years=1))).all()
    temp=dict(temps)
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start(start='2015-01-01',end='2018-12-31'):
    a=session.query(Measurement.tobs).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    b=[]
    for i in a:
        b.append(i[0])
    values=[min(b),np.mean(b),max(b)]
    return jsonify(values)

if __name__ == '__main__':
    app.run(debug=True)
