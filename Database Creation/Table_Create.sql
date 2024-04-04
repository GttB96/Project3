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

CREATE TABLE stations(
	State VARCHAR,
	BD int,
	CNG int,
	E85 int,
	Electric int,
	Hydrogen int,
	LNG int,
	LPG int,
	RD int,
	PRIMARY KEY (State)
);