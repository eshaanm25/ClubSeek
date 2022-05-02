from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from get_docker_secret import get_docker_secret
import clubseek.api

'''
Initialize Flask API and connect to Database
'''


# Get DB Username and Password from Docker Secrets
dbURI = get_docker_secret('db_uri')

# Configure API Endpoint
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.register_blueprint(clubseek.api.apiEndpoints) # Register API Endpoints from api.py
db = SQLAlchemy(app) # Define DB bject for creating DB Sessions

# Start API Endpoint
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)

# SQL Alchemy DB Class for Communicating with Bars Table 

class Bars(db.Model):
    __tablename__ = "Bars"

    address = db.Column(db.String(255), primary_key = True)
    barName = db.Column(db.String(30), primary_key = True)
    capacity = db.Column(db.Integer)
    currentTraffic = db.Column(db.Integer)
    wowFactor = db.Column(db.Integer)

# SQL Alchemy DB Class for Communicating with Users Table 
class Users(db.Model):
    __tablename__ = "Users"

    userName = db.Column(db.String(255), primary_key = True)
    userPhoneNumber = db.Column(db.String(15), primary_key = True)
    assignedBarName = db.Column(db.String(30))
    assignedBarAddress = db.Column(db.String(255))
