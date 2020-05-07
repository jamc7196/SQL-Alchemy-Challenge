#Student: Jorge Alberto Muñozcano Castro
#SQL ALCHEMY

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#1)Setup database using Engine and autobase
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn =engine.connect
Base = automap_base()
Base.prepare(engine, reflect=True)
#2)Get the index variables from the Base and create a session
Measurements = Base.classes.measurement
Stations = Base.classes.station
session = Session(engine)
#3)Setup Flask
app = Flask(__name__)

#4)Setup Flask routes
#First route main menu route
@app.route("/")
def main_menu():
    """List of all the available API routes."""
    return (
        f"Student: Jorge Alberto Muñozcano Castro <br/>"
        f"SQL-Challenge: Part 2 Flask <br/>"
        f"--------------------------------------------<br/>"
        f"Hawaii Weather Control Center:<br/>"
        f"Available Routes:<br/>"
        f"--------------------------------------------<br/>"
        f"1)Precipitation: /api/v1.0/precipitation<br/>"
        f"2)Stations: /api/v1.0/stations<br/>"
        f"3)Temperature observation for 1 year: /api/v1.0/tobs<br/>"
        f"4)Temperature stats from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"5)Temperature stats from start to the lastdate(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )
#Second route: precipitation 
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    Precip_score = [Measurements.date,Measurements.prcp]
    precipitation_results = session.query(*Precip_score).all()
    session.close()
    precipitation = []
    for date, prcp in precipitation_results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)
    return jsonify(precipitation)
#Third route: stations
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    active_stations = [Stations.station,Stations.name,Stations.latitude,Stations.longitude,Stations.elevation]
    stations_results = session.query(*active_stations).all()
    session.close()
    stations = []
    for station,name,lat,lon,el in stations_results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)
    return jsonify(stations)
#Fourth Temperature Observation
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    temp_first_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()[0]
    temp_last_date = dt.datetime.strptime(temp_first_date, '%Y-%m-%d')
    last_date_query = dt.date(temp_last_date.year -1, temp_last_date.month, temp_last_date.day)
    temp_obs = [Measurements.date,Measurements.tobs]
    temp_obs_results = session.query(*temp_obs).filter(Measurements.date >= last_date_query ).all()
    session.close()
    temp_obs = []
    for date, tobs in temp_obs_results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        temp_obs.append(tobs_dict)
    return jsonify(temp_obs)
#Fifth route: Temperature Stats from the Start Date
@app.route('/api/v1.0/<start_date>')
def get_temp_start(start_date):
    session = Session(engine)
    start_date_results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    session.close()
    temp_obs_fd = []
    for min, avg, max in start_date_results:
        tobs_dict1 = {}
        tobs_dict1["Minimum"] = min
        tobs_dict1["Average"] = avg
        tobs_dict1["Maximum"] = max
        temp_obs_fd.append(tobs_dict1)
    return jsonify(temp_obs_fd)

#Sixth route: Temperature Stats from the Start Date
@app.route('/api/v1.0/<start_date>/<end_date>')
def get_temp_start_stop(start_date,end_date):
    session = Session(engine)
    last_date_results= session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
    session.close()
    temp_obs_ld = []
    for min,avg,max in last_date_results:
        tobs_dict2 = {}
        tobs_dict2["Minimum"] = min
        tobs_dict2["Average"] = avg
        tobs_dict2["Maximum"] = max
        temp_obs_ld.append(tobs_dict2)
    return jsonify(temp_obs_ld)

#5)Generate Flask
if __name__ == "__main__":
    app.run(debug=True)
        
    
    