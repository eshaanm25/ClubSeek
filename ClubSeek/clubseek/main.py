from multiprocessing.connection import wait
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import time


def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='clubdatabases',
            user=user_name,
            passwd=user_password,
            db = 'clubdatabase'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred. Attempting to reconnect")
        time.sleep(5)

    return connection

connection = None
while connection == None:
    connection = create_connection("127.0.0.1", "user", "password")

# Initialize Application
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return jsonify({ 'msg': 'Hello World'})

# Run Server
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=3000)