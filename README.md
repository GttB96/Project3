## Project3 Group 3 - EV Charging Stations Data And Analysis

## Project Description
### Using public data found on https://afdc.energy.gov/stations/states we will be doing an analysis and visualization of electric charging stations in the US, alongside historical data spanning 2014-2023.

## Instructions to run on local machine

### Clone repository to desired folder - [git clone https://github.com/GttB96/Project3.git]
### Activate dev environment - [conda activate dev]
### Data_Upload:
#### Download csv files [Current_Alt_Fuel_locations.csv] [all_historical.csv] from /CleanedData For PostgresSQL

### Data Import to Postgres SQL:
#### Open PostGres and Create New Database - [Project3] 
##### (SQL_Create_Project3Database.sql)

#### Import Table_Create.sql from /Database_Tables Creation Scripts to pgAdmin to create tables
#### Import csv files into database tables in Postgres manually - or copy the files to the Postgres data directory and import using SQL_ImportData.sql (instructions in sql script)
#####        [Current_Alt_Fuel_locations.csv] to stations & [all_historical.csv] to all_historical

### Library Requirements:
#### Install Flask-SQLAlchemy in project directory - [pip install Flask-SQLAlchemy]
#### Install DotEnv Package in project directory - [pip install python-dotenv]
#### Install psycopg2 in project directory - [pip install psycopg2-binary]
#### Update watchdog in project directory - [pip install --upgrade watchdog]

#### create .env file (touch .env .gitignore) on repository and input in file: [DATABASE_URL=postgresql://username:password@localhost/Project3]
##### **(change username & password with your own)**

#### Run python app.py in terminal on repository to execute the application
#### http://127.0.0.1:5000/

### Data Source:
#### U.S Department of ENERGY|Energy Efficiency & Renewable Energy – Alternate Fuels Data Center
#### https://afdc.energy.gov/stations/states

### Ethical Considerations
#### The ethical concerns around this application are low. Considering we are not storing any personal information or need any personal information for the application to function the risk for a data leak or breach is very low. On the other hand, the security used in the application is weak which could lead to potential threats if made available outside your local network. The application does require username and password for the database, the username and password used in this application is stored on an .env files which is ignored in github thus minimizing risk to user data. 


