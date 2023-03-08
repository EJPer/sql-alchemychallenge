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


#Create an app
app = Flask(__name__)

#Listing Home page and possible routes
@app.route("/")
def home():
    print("recieved request for 'Home Page...")
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

    last_12_months = session.query(Measurment.date,Measurment.prcp).\
    filter(Measurment.date > year_early).all()
    
    return last_12_months

    session.close()

    # #Create a dict, from the rows of data
    # percip = []
    # for date, prcp in last_12_months:
    #     percip_dict = {}
    #     percip_dict["date"] = date
    #     percip_dict["prcp"] = prcp
    #     percip.append(percip_dict)



    # return jsonify(precip)





if __name__ == "__main__":
    app.run(debug=True)




