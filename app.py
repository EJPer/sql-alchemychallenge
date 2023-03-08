#Import Flask
from flask import Flask

#Create an app
app = Flask(__name__)

#Define index route
@app.route("/")
def home():
    print("recieved request for 'Home Page...")
    return("welcome to home page see possible routes below:<br/>"
    f"Use Path /api/v1.0/precipitation for precipitation analysis<br/>"
    f"Use Path /api/v1.0/stations<br/>"
    f"Use Path /api/v1.0/tobs for temp analysis<br/>" 
    f"Use Path /api/v1.0/<start> and /api/v1.0/<start>/<end> to observe min max temps throughout those dates<br/> "
    
    )

if __name__ == "__main__":
    app.run(debug=True)
