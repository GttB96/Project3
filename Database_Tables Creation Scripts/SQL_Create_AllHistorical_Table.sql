-- Database: Project3

--DROP DATABASE IF EXISTS "Project3";


CREATE DATABASE "Project3"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;



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





select * from all_historical;





