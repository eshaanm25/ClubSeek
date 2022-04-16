from multiprocessing.connection import wait
from flask import Flask, Blueprint, request, jsonify
from database import create_connection
from api import apiEndpoints

# Initialize DB Connection
connection = None
while connection == None:
    connection = create_connection("user", "password")

# Run Server
if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(apiEndpoints)
    app.run(debug=True,host='0.0.0.0', port=3000)