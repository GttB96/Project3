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