from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
from flask import request, jsonify
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##defining columns of data

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

##First page rendering
@app.route('/')
def index_page():
    return render_template('index.html')

##Map page rendering
@app.route('/map')
def stations_map():
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

##Defining regions
regions = {
    'Northeast': ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA'],
    'Midwest': ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI'],
    'South': ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'DC', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX'],
    'West': ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']
}

##Station data rendering
@app.route('/station')
def station_page():
    # Getting stations by state
    state_query = text("""
    SELECT state, COUNT(*) AS count 
    FROM stations 
    WHERE fueltypecode = 'ELEC' 
    GROUP BY state
    """)
    state_result = db.session.execute(state_query).mappings()
    states_data = [{'state': row['state'], 'count': row['count']} for row in state_result]

    # Getting stations by city
    city_query = text("""
    SELECT city, state, COUNT(*) AS count 
    FROM stations 
    WHERE fueltypecode = 'ELEC' 
    GROUP BY city, state 
    ORDER BY count DESC 
    LIMIT 50
    """)
    city_result = db.session.execute(city_query).mappings()
    cities_data = [{'city': row['city'], 'state': row['state'], 'count': row['count']} for row in city_result]

    # Getting states by region
    region_counts = {region: 0 for region in regions}
    for state_data in states_data:
        for region, states in regions.items():
            if state_data['state'] in states:
                region_counts[region] += state_data['count']

    # Convert region_counts dict to a list of dicts for easier processing in the template
    regions_data = [{'region': region, 'count': count} for region, count in region_counts.items()]

    return render_template('station.html', states_data=states_data, cities_data=cities_data, regions_data=regions_data)

if __name__ == '__main__':
    app.run(debug=True)
