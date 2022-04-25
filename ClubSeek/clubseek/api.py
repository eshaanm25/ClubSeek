from calendar import c
from tabnanny import check
from flask import Blueprint, request, jsonify, make_response
from flask_expects_json import expects_json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from constants import *
from database import connection

apiEndpoints = Blueprint('apiEndpoints',__name__)

# Readiness Probe 
@apiEndpoints.route('/readiness', methods=['GET'])
def readiness():
    try:
        with connection.begin() as conn:
            checkBars = conn.execute(
                text("SELECT 1")
        )
        
        # Make Successful Response
        returnString = "Ready"
        response = make_response(returnString, 200)

        return(response)

    except SQLAlchemyError as e:

        # Make Unsuccessful Response
        returnString = "ClubSeek is waiting for the MySQL Database to start. Connection status: %s" % (e)
        response = make_response(returnString, 502)
        response.mimetype = "text/html"

        return(response)

# Add Bars to Database
@apiEndpoints.route('/bars', methods=['PUT'])
@expects_json(barSchema)
def add_bar():
    # Get Values from Request 
    values = request.get_json()

    #Check if Row Exists
    with connection.connect() as conn:
        checkBars = conn.execute(
            text("SELECT * FROM Bars WHERE barName = '%s'" % (values["barName"]))
        )

    if checkBars.all() == []:
        # Assemble Data to add to DB
        insert_stmt = "INSERT INTO Bars (barName, wowFactor, capacity, currentTraffic, address) VALUES ('%s', '%s', '%s', '%s', '%s')" % (values["barName"], values["wowFactor"], values["capacity"], values["currentTraffic"], values["address"])
        
        # Add data to DB
        with connection.begin() as conn:
            checkBars = conn.execute(
                text(insert_stmt)
        )

        # Make Response
        returnString = "Success! <b>%s</b> was added to the list of Bars. <br> Run a GET method on the /bars endpoint to see all Bars." % (values["barName"])
        response = make_response(returnString, 200)
        response.mimetype = "text/html"

        return(response)
    else:
        returnString = "The bar <b>%s</b> was already added to the list of Bars." % (values["barName"])
        response = make_response(returnString, 300)
        response.mimetype = "text/html"
        return(response)


# Get all Bars from Database
@apiEndpoints.route('/bars', methods=['GET'])
def get_bar():

    # Get Data from Database
    with connection.connect() as conn:
        barsGet = conn.execute(
            text("SELECT * FROM Bars")
        )
    
    bars = barsGet.all()
    
    if bars == []:
        # Make Response that Table is Empty
        returnString = "There are no Bars yet! <br> Add a bar using the POST method on the /bar endpoint. <br> See README for request body schema."
        response = make_response(returnString, 300)
        response.mimetype = "text/html"
        return(response)

 
    # Make Response with all Bars as a Dictionary
    allBarsDictionary = []
    for bar in bars:
        barDictionary = dict(barName = bar[0], wowFactor=bar[1], capacity=bar[2],  currentTraffic=bar[3], address=bar[4])
        allBarsDictionary.append(barDictionary)

    return jsonify(allBarsDictionary)

# Delete Bar from Database
@apiEndpoints.route('/bars', methods=['DELETE'])
@expects_json(barDeleteSchema)
def del_bar():
    # Get Values from Request   
    values = request.get_json()

    #Check if Row Exists 
    checkStatement = "SELECT * FROM Bars WHERE barName = '%s'" % (values["barName"])

    with connection.connect() as conn:
        checkBars = conn.execute(
            text(checkStatement)
        )

    if checkBars.all() == []:
        # Make Response that Bar does not Exist
        returnString = "This Bar Does not Exist in the Database! <br> See existing bars using the GET method on the /bars endpoint."
        response = make_response(returnString, 300)
        response.mimetype = "text/html"
        return(response)
    else:
        # Delete Bar from Database
        deleteStatement = "DELETE FROM Bars WHERE barName='%s'" % (values["barName"])
        with connection.begin() as conn:
            checkBars = conn.execute(
                text(deleteStatement)
            )

        # Make Response
        returnString = "Success! <b>%s</b> was deleted from the list of Bars. <br> Run a GET method on the /bars endpoint to see all Bars." % (values["barName"])
        response = make_response(returnString, 200)
        response.mimetype = "text/html"

        return(response)