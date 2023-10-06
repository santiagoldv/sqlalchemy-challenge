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
        f"Hawaii info you want to check if traveling!<br/>"
        f"/precipitation - Precipitation analysis 2016-2017<br/>"
        f"/stations - Stations list<br/>"
        f"/tobs - Temperature observations in the most active season (2016 - 2017)<br/>"
        f"/start - Temperature stats for the most active season (2016 - 2017)<br/>"
        f"/start/end - Temperature statistics in certain range"
    )






if __name__ == "__main__":
    app.run(debug=True)