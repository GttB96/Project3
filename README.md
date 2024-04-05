# Project3

## Instructions to run on local machine

### Clone repository to desired folder - git clone https://github.com/GttB96/Project3.git

### Data_Upload:
#### Download csv files [Current_Alt_Fuel_locations.csv] [all_historical.csv] from Data_For_PostgresSQL
#### Open PostGres and Create New Database - Project3

#### Import Table_Create.sql file to pg admin to create tables
#### Import csv files into database tables in Postgres
##### [Current_Alt_Fuel_locations.csv] to stations & [all_historical.csv] to all_historical

### Library Requirements:
#### Install Flask-SQLAlchemy in project directory - pip install Flask-SQLAlchemy
#### Install DotEnv Package in project directory - pip install python-dotenv
#### Install psycopg2 in project directory - pip install psycopg2-binary
#### Update watchdog in project directory - pip install --upgrade watchdog
#### create .env file on repository and input in file: DATABASE_URL=postgresql://username:password@localhost/Project3
##### **(change username & password with your own)**
#### Run python app.py in terminal on repsoitory to execute the application