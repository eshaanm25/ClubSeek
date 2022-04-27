from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from get_docker_secret import get_docker_secret
from api import apiEndpoints

# Get Docker Secrets
dbUsername = get_docker_secret('db_user')
dbPassword = get_docker_secret('db_password')

# Configure API Endpoint
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@clubdatabases:3306/clubdatabase' % (dbUsername, dbPassword)
app.register_blueprint(apiEndpoints)
db = SQLAlchemy(app)

# Run API Endpoint
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=3000)
