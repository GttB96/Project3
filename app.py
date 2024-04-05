from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AllHistorical(db.Model):
    __tablename__ = 'all_historical'
    state = db.Column(db.String, primary_key=True)
    year = db.Column(db.Numeric, primary_key=True)
    biodiesel = db.Column(db.Numeric)
    cng = db.Column(db.Numeric)
    e85 = db.Column(db.Numeric)
    electricstations = db.Column(db.Numeric)
    electricchargingoutlets = db.Column(db.Numeric)
    electrictotal = db.Column(db.Numeric)
    hydrogenretail = db.Column(db.Numeric)
    hydrogennonretail = db.Column(db.Numeric)
    hydrogentotal = db.Column(db.Numeric)
    lng = db.Column(db.Numeric)
    propaneprimary = db.Column(db.Numeric)
    propanesecondary = db.Column(db.Numeric)
    propanetotal = db.Column(db.Numeric)
    total = db.Column(db.Numeric)

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    fueltypecode = db.Column(db.String(4))
    streetaddress = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip = db.Column(db.String(7))
    latitude = db.Column(db.Numeric(9, 6))
    longitude = db.Column(db.Numeric(9, 6))
    stationname = db.Column(db.String(255))
    maximumvehicleclass = db.Column(db.String(3))
    accesscode = db.Column(db.String(255))
    facilitytype = db.Column(db.String(255))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def stations():
    sql = """
    SELECT streetaddress AS "street_address", city, state, zip, latitude, longitude, fueltypecode,
           COUNT(*) AS station_count
    FROM stations
    WHERE fueltypecode = 'ELEC'
    GROUP BY streetaddress, city, state, zip, latitude, longitude, fueltypecode
    ORDER BY COUNT(*) DESC
    LIMIT 1000
    """
    result = db.session.execute(text(sql))
    stations_by_address = [dict(row) for row in result.mappings()]
    return render_template('map.html', stations_by_address=stations_by_address)

@app.route('/station.html')
def pie_chart_fuel():
    sql = """
    """
    
if __name__ == '__main__':
    app.run(debug=True)
