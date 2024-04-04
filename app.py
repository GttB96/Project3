from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
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

class Stations(db.Model):
    __tablename__ = 'stations'
    state = db.Column(db.String, primary_key=True)
    bd = db.Column(db.Integer)
    cng = db.Column(db.Integer)
    e85 = db.Column(db.Integer)
    electric = db.Column(db.Integer)
    hydrogen = db.Column(db.Integer)
    lng = db.Column(db.Integer)
    lpg = db.Column(db.Integer)
    rd = db.Column(db.Integer)

@app.route('/')
def index():
    # Fetch the first 10 records
    data = AllHistorical.query.limit(10).all()
    return render_template('test.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
