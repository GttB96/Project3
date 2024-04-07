from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
from flask import request, jsonify
from sqlalchemy import func
import os

## need to load in .env file with secure credentials
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Defining columns of data

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
    # Query for individual stations
    sql_stations = """
    SELECT streetaddress AS "street_address", city, state, zip, latitude, longitude, fueltypecode, stationname, facilitytype,
           COUNT(*) AS station_count
    FROM stations
    WHERE fueltypecode = 'ELEC' AND accesscode = 'public'
      AND (maximumvehicleclass = 'LD' OR maximumvehicleclass IS NULL)
    GROUP BY streetaddress, city, state, zip, latitude, longitude, fueltypecode, stationname, facilitytype
    ORDER BY COUNT(*) DESC
    LIMIT 5000;
    """
    stations_result = db.session.execute(text(sql_stations))
    stations_by_address = [dict(row) for row in stations_result.mappings()]

    # Query for aggregating stations by city for heatmap
    sql_cities = """
    SELECT city, state, AVG(latitude) AS avg_latitude, AVG(longitude) AS avg_longitude, COUNT(*) AS station_count
    FROM stations
    WHERE fueltypecode = 'ELEC' AND accesscode = 'public' 
          AND (maximumvehicleclass = 'LD' OR maximumvehicleclass IS NULL)
    GROUP BY city, state;
    """
    cities_result = db.session.execute(text(sql_cities))
    cities_aggregated = [dict(row) for row in cities_result.mappings()]

    # Pass both datasets to the template
    return render_template('map.html', stations_by_address=stations_by_address, cities_aggregated=cities_aggregated)

# Route to find nearest station function
@app.route('/find-nearest-station', methods=['GET'])
def find_nearest_station():
    user_zip = request.args.get('zip')

    # Query to find stations with the same zip code
    stations_query = text("""
    SELECT id, streetaddress, city, state, zip, latitude, longitude, fueltypecode, stationname, facilitytype,
    (SELECT COUNT(*) 
     FROM stations AS s 
     WHERE s.fueltypecode = 'ELEC' AND s.zip = :zip_code
    ) AS station_count
    FROM stations
    WHERE fueltypecode = 'ELEC' AND zip = :zip_code
    LIMIT 1
    """)
    station_result = db.session.execute(stations_query, {'zip_code': user_zip}).fetchone()

    if station_result:
        station_count = db.session.query(func.count(Station.id)).filter_by(fueltypecode=station_result.fueltypecode, zip=station_result.zip).scalar()

        # Need to convert to a dictionary to render in javascript
        station_dict = {
            "id": station_result.id,
            "streetaddress": station_result.streetaddress,
            "city": station_result.city,
            "state": station_result.state,
            "zip": station_result.zip,
            "latitude": float(station_result.latitude),
            "longitude": float(station_result.longitude),
            "fueltypecode": station_result.fueltypecode,
            "stationname": station_result.stationname,
            "facilitytype": station_result.facilitytype,
            "station_count": station_count
        }
        return jsonify(station_dict)
    else:
        return jsonify({"error": "No stations found in this zip code."})

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
    WHERE fueltypecode = 'ELEC' AND accesscode = 'public' AND (maximumvehicleclass = 'LD' OR maximumvehicleclass IS NULL)
    GROUP BY state
    """)
    state_result = db.session.execute(state_query).mappings()
    states_data = [{'state': row['state'], 'count': row['count']} for row in state_result]

    # Getting stations by city
    city_query = text("""
    SELECT city, state, COUNT(*) AS count 
    FROM stations 
    WHERE fueltypecode = 'ELEC' AND accesscode = 'public' AND (maximumvehicleclass = 'LD' OR maximumvehicleclass IS NULL)
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

    regions_data = [{'region': region, 'count': count} for region, count in region_counts.items()]

    facilitytype_query = text("""
    SELECT facilitytype, COUNT(*) AS count 
    FROM stations 
    WHERE fueltypecode = 'ELEC' 
    AND accesscode = 'public' 
    AND (maximumvehicleclass = 'LD' OR maximumvehicleclass IS NULL)
     AND facilitytype IS NOT NULL -- Exclude null values
    GROUP BY facilitytype
    ORDER BY count DESC -- Sort by count in descending order
    LIMIT 20
    """)
    facilitytype_result = db.session.execute(facilitytype_query).mappings()
    facilitytype_data = [{'facilitytype': row['facilitytype'], 'count': row['count']} for row in facilitytype_result]

    return render_template('station.html', states_data=states_data, cities_data=cities_data, regions_data=regions_data, facilitytype_data=facilitytype_data)

if __name__ == '__main__':
    app.run(debug=True)
