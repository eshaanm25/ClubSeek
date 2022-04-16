import mysql.connector
from mysql.connector import Error
import time

def create_connection(user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='clubdatabases',
            user=user_name,
            passwd=user_password,
            db = 'clubdatabase'
        )

        try:
            mycursor = connection.cursor()
            mycursor.execute("CREATE TABLE Bars (barName varchar(255), wowFactor int, capacity int, currentTraffic int, PRIMARY KEY(barName));")
            mycursor.close()
            connection.commit()
        except mysql.connector.Error as err:
            print("Error Occurred or Table Already Exists: {}".format(err))
            pass

        print("Connection to MySQL DB successful")
    except Error as e:
        print("The error %s occurred. Attempting to reconnect" % (e))
        time.sleep(5)

    return connection