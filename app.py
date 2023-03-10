#Import Flask
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from datetime import date
from datetime import datetime



##################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect db into new model
Base = automap_base()

#reflect the tables
Base.prepare(autoload_with = engine)

Measurment = Base.classes.measurement
Station = Base.classes.station

##input start and end dates





#Create an app
app = Flask(__name__)

#Listing Home page and possible routes
@app.route("/")
def home():
    print("recieved request for 'Home Page...")
    """List all available routes"""
    return("welcome to home page see possible routes below:<br/>"
    f"Use Path /api/v1.0/precipitation for precipitation analysis<br/>"
    f"Use Path /api/v1.0/stations<br/>"
    f"Use Path /api/v1.0/tobs for temp analysis<br/>" 
    f"Use Path /api/v1.0/<start> and /api/v1.0/<start>/<end> to observe min max temps throughout those dates<br/> "
    )

@app.route("/api/v1.0/precipitation")
def precip():
    #Create session link from python to Db
    session =  Session(engine)

    #to get last year's date
    finaldate = session.query(Measurment.date).order_by(Measurment.date.desc()).first()
    year_early = datetime.strptime(finaldate[0], '%Y-%m-%d') - dt.timedelta(days = 365)

    last_12_months = session.query(Measurment.date,Measurment.prcp).filter(Measurment.date >= year_early).all()

    session.close()

    #Create a dict, from the rows of data
    precip = dict(last_12_months)


    return jsonify(precip)


#################################
#next path
#################################
@app.route("/api/v1.0/stations")
def stations():
    #create session link to db
    session = Session(engine)

    #query for station list
    station_list = active_stations = session.query(Station.station).all()

    session.close()

    #create list:
    final_list = list(np.ravel(station_list))

    return jsonify(final_list)

#################################
#next path
#################################
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #query 
    finaldate = session.query(Measurment.date).order_by(Measurment.date.desc()).first()
    year_early = datetime.strptime(finaldate[0], '%Y-%m-%d') - dt.timedelta(days = 365)


    high_station_query = session.query(Measurment.date, Measurment.tobs).filter(Measurment.station == 'USC00519281').filter(Measurment.date >= year_early).all()

    session.close()
    
    #create a dictionary:
    active_station = dict(high_station_query)

    return jsonify(active_station)



#################################
#next path-dynamic
#################################
@app.route("/api/v1.0/<start>")
def date_start(start):
     #create session
     session = Session(engine)
     date_format = '%Y-%m-%d'
     dt.datetime.strptime(start, date_format)
     results = session.query(Measurment.date,func.avg(Measurment.tobs),func.max(Measurment.tobs), func.min(Measurment.tobs)).filter(Measurment.date >= (start)).group_by(Measurment.date).all()
     


     session.close()
     
     start_results = []
     for output in results:
         start_dict={}
         start_dict['date'] = output[0]
         start_dict['Avg temp'] = output[1]
         start_dict['Max temp'] = output[2]
         start_dict['Min Temp'] = output[3]
         start_results.append(start_dict)
         
       
     return jsonify(start_results)




#################################
#next path-dynamic
#################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    #create session
    session = Session(engine)
    #format starting and end dates
    date_format = '%Y-%m-%d'
    start_format = dt.datetime.strptime(start, date_format)
    end_format = dt.datetime.strptime(end, date_format)

    #query
    results = session.query(Measurment.date,func.avg(Measurment.tobs),func.max(Measurment.tobs), func.min(Measurment.tobs)).filter(Measurment.date >= (start_format)).filter(Measurment.date <= (end_format)).group_by(Measurment.date).all()


    session.close()

    start_end_results = []
    for output in results:
         start_end_dict={}
         start_end_dict['date'] = output[0]
         start_end_dict['Avg temp'] = output[1]
         start_end_dict['Max temp'] = output[2]
         start_end_dict['Min Temp'] = output[3]
         start_end_results.append(start_end_dict)
         
       
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)

    