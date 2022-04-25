from sqlite3 import connect
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

import time
from get_docker_secret import get_docker_secret

dbUsername = get_docker_secret('db_user')
dbPassword = get_docker_secret('db_password')
connection = create_engine('mysql+pymysql://%s:%s@clubdatabases:3306/clubdatabase' % (dbUsername, dbPassword))

# Connect to Database
while True:
    try:
        with connection.begin() as conn:
            checkBars = conn.execute(
                text("SELECT 1")
        )
        print("Connection to MySQL DB successful")
        break
    except SQLAlchemyError as e:
        print("ClubSeek is waiting for the MySQL Database to start. Connection status: %s" % (e))
        time.sleep(5)
        continue
