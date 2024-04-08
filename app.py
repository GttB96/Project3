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
 SELECT 
    id, streetaddress AS "street_address", city, state, zip, latitude, longitude, 
    fueltypecode, stationname, facilitytype
FROM 
    stations
WHERE 
    fueltypecode = 'ELEC' 
    AND accesscode = 'public'
    AND (maximumvehicleclass = 'LD' OR maximumvehicleclass IS NULL)
    AND state <> 'PR'
    AND LENGTH(zip) = 5 -- Ensure ZIP codes are 5 digits
    AND zip NOT LIKE '%.0' -- Exclude ZIP codes ending in ".0"
ORDER BY RANDOM()
LIMIT 10000;
    """
    stations_result = db.session.execute(text(sql_stations))
    stations_by_address = [dict(row) for row in stations_result.mappings()]

    # Query for aggregating stations by city for heatmap
    all_stations = """
 SELECT 
    id, streetaddress AS "street_address", city, state, zip, latitude, longitude, 
    fueltypecode, stationname, facilitytype
FROM 
    stations
WHERE 
    fueltypecode = 'ELEC' 
    AND accesscode = 'public'
    AND (maximumvehicleclass = 'LD' OR maximumvehicleclass IS NULL)
    AND state <> 'PR'
    AND LENGTH(zip) = 5 -- Ensure ZIP codes are 5 digits
    AND zip NOT LIKE '%.0'; -- Exclude ZIP codes ending in ".0"
    """
    stations_result = db.session.execute(text(all_stations))
    stationsDataAll = [dict(row) for row in stations_result.mappings()]

    # Pass both datasets to the template
    return render_template('map.html', stations_by_address=stations_by_address, stationsDataAll=stationsDataAll)

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

@app.route('/historical')
def historical_USA():
    sql = """
    SELECT year, SUM(electricstations) AS total_electric_stations
    FROM all_historical
    GROUP BY year
    ORDER BY year
    """
    result = db.session.execute(text(sql))
    historical_data = [dict(row) for row in result.mappings()]

    start_value = next((item for item in historical_data if item["year"] == 2014), None)
    end_value = next((item for item in historical_data if item["year"] == 2023), None)
    
    if start_value and end_value:
        # Convert Decimal to float for calculation
        start_stations = float(start_value["total_electric_stations"])
        end_stations = float(end_value["total_electric_stations"])
        years = 2023 - 2014

        # Use float type for both base and exponent in the power operation
        cagr = ((end_stations / start_stations) ** (1 / years)) - 1
        cagr_percentage = round(cagr * 100, 2)
    else:
        cagr_percentage = None

    yoy_growth = []
    for i in range(1, len(historical_data)):
        year = historical_data[i]["year"]  # Current year
        current_year_stations = float(historical_data[i]["total_electric_stations"])
        previous_year_stations = float(historical_data[i-1]["total_electric_stations"])
        growth_rate = ((current_year_stations - previous_year_stations) / previous_year_stations) * 100
        yoy_growth.append({"year": year, "growth": round(growth_rate, 2)})

    if start_value and end_value:
        # Assuming start_value and end_value are already defined for CAGR calculation
        start_stations = float(start_value["total_electric_stations"])
        end_stations = float(end_value["total_electric_stations"])
        
        # Calculating total growth
        total_growth = ((end_stations - start_stations) / start_stations) * 100
        total_growth_percentage = round(total_growth, 2)
    else:
        total_growth_percentage = None

    return render_template('historical.html', historical_data=historical_data, cagr_percentage=cagr_percentage, yoy_growth=yoy_growth, total_growth_percentage=total_growth_percentage)

if __name__ == '__main__':
    app.run(debug=True)
