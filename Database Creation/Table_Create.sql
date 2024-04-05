DROP TABLE IF EXISTS all_historical;

CREATE TABLE all_historical(
	State VARCHAR,
	Year decimal,
	Biodiesel decimal,
	CNG decimal,
	E85 decimal,
	ElectricStations decimal,
	ElectricChargingOutlets decimal,
	ElectricTotal decimal,
	HydrogenRetail decimal,
	HydrogenNonRetail decimal,
	HydrogenTotal decimal,
	LNG decimal,
	PropanePrimary decimal,
	PropaneSecondary decimal,
	PropaneTotal decimal,
	Total decimal,
	PRIMARY KEY (State, Year)
);

DROP TABLE IF EXISTS stations;

CREATE TABLE stations (
    ID SERIAL PRIMARY KEY,
    FuelTypeCode CHAR(4),
    StreetAddress VARCHAR(255),
    City VARCHAR(100),
    State CHAR(2),
    ZIP CHAR(7),
    Latitude NUMERIC(9, 6),
    Longitude NUMERIC(9, 6),
    StationName VARCHAR(255),
    MaximumVehicleClass CHAR(3),
    AccessCode VARCHAR(255),
    FacilityType VARCHAR(255)
);
