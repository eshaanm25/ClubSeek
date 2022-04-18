import mysql.connector
from mysql.connector import Error
import time
from get_docker_secret import get_docker_secret

def add_tables(connection):
    try:
        mycursor = connection.cursor()
        mycursor.execute("CREATE TABLE Bars (barName varchar(255), wowFactor int, capacity int, currentTraffic int, address varchar(255), PRIMARY KEY(barName));")
        mycursor.close()
        connection.commit()
    except mysql.connector.Error as err:
        print("Error Occurred or Table Already Exists: {}".format(err))
        pass

dbUsername = get_docker_secret('db_user')
dbPassword = get_docker_secret('db_password')

while True:
    try:
        connection = mysql.connector.connect(
            host='clubdatabases',
            user= dbUsername,
            passwd= dbPassword,
            db = 'clubdatabase'
        )
        print("Connection to MySQL DB successful")
        add_tables(connection)
        break
    except Error as e:
        print("ClubSeek is waiting for the MySQL Database to start. Connection status: %s" % (e))
        time.sleep(5)
        continue
