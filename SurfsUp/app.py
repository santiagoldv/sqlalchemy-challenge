# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def home():
    return (
        f"Climate analysis for vacacions in Hawaii<br/>"
        f"<br/>"
        f"All available routes: <br/>"
        f".../precipitation - Precipitation analysis 2016-2017.<br/>"
        f".../stations - Stations list.<br/>"
        f".../tobs - Temperatures observations in the most active season (2016 - 2017).<br/>"
        f".../start - Temperatures from specific start to end of year, please insert date YYYY-MM-DD after local host: (http://localhost.../YYYY-MM-DD).<br/>"
        f".../start/end - Temperatures from specific range, please insert start first and then end of range (YYYY-MM-DD) after local host: (http://localhost.../YYYY-MM-DD/YYYY-MM-DD)."
    )

@app.route("/precipitation")
def precipitation():
    date_leap = "2016-08-23"
    leap = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_leap).all()
    prcp_list = []

    for date, prcp in leap:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)
    session.close()

@app.route("/stations")
def stations():
    station_list = session.query(Station.station).all()
    stations = [station[0] for station in station_list]
    return jsonify(stations)
    session.close()

@app.route("/tobs")
def tobs():
    station = "USC00519281"
    date = "2016-08-23"
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == station).filter(Measurement.date >= date).group_by(Measurement.date).order_by(Measurement.date).all()
    tobs_list = []

    for date, tobs in tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)
    session.close()

@app.route("/<start>")
def start_date(start):
    temp_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    min_temp, max_temp, avg_temp = temp_start[0]
    temp_start_dict = {"Consulted Date": start, "Minimum Temperature": min_temp, "Maximum Temperature": max_temp, "Average Temperature": avg_temp}
    return jsonify(temp_start_dict)
    session.close()


@app.route("/<start>/<end>")
def start_end_date(start, end):
    # Design the query to calculate the temperature statistics in the given date range
    start_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    min_temp, max_temp, avg_temp = start_end[0]
    temperature_range_dict = {"Start Date": start, "End Date": end, "Minimum Temperature": min_temp, "Maximum Temperature": max_temp, "Average Temperature": avg_temp}
    return jsonify(temperature_range_dict)
    session.close()

if __name__ == "__main__":
    app.run(debug=True)