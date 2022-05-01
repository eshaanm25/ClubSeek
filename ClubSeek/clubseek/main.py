from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from get_docker_secret import get_docker_secret
from api import apiEndpoints

'''
Initialize Flask API and connect to Database
'''


# Get DB Username and Password from Docker Secrets
dbURI = get_docker_secret('db_uri')

# Configure API Endpoint
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.register_blueprint(apiEndpoints) # Register API Endpoints from api.py
db = SQLAlchemy(app) # Define DB bject for creating DB Sessions

# Start API Endpoint
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
