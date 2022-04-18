from flask import Blueprint, request, jsonify, make_response
from flask_expects_json import expects_json
from constants import *
from database import connection

apiEndpoints = Blueprint('apiEndpoints',__name__)

# Add Bars to Database
@apiEndpoints.route('/bars', methods=['POST'])
@expects_json(barSchema)
def add_bar():
    # Get Values from Request 
    values = request.get_json()

    # Initiate Database Cursor
    mycursor = connection.cursor()

    # Assemble Data to add to DB
    insert_stmt = (
    "INSERT INTO Bars (barName, wowFactor, capacity, currentTraffic, address) "
    "VALUES (%(barName)s, %(wowFactor)s, %(capacity)s, %(currentTraffic)s, %(address)s)"
    )
    
    # Add data to DB
    mycursor.execute(insert_stmt, values)
    mycursor.close()
    connection.commit()

    # Make Response
    returnString = "Success! <b>%s</b> was added to the list of Bars. <br> Run a GET method on the /bars endpoint to see all Bars." % (values["barName"])
    response = make_response(returnString, 200)
    response.mimetype = "text/html"

    return(response)

# Get all Bars from Database
@apiEndpoints.route('/bars', methods=['GET'])
def get_bar():
    # Initiate Database Cursor
    mycursor = connection.cursor()

    # Get Data from Database
    mycursor.execute("SELECT * FROM Bars")
    allBars = mycursor.fetchall()
    
    if allBars == []:
        # Make Response that Table is Empty
        returnString = "There are no Bars yet! <br> Add a bar using the POST method on the /bar endpoint. <br> See README for request body schema."
        response = make_response(returnString, 200)
        response.mimetype = "text/html"
        return(response)

    # Make Response with all Bars as a Dictionary
    allBarsDictionary = []
    for bar in allBars:
        barDictionary = dict(barName = bar[0], wowFactor=bar[1], capacity=bar[2],  currentTraffic=bar[3], address=bar[4])
        allBarsDictionary.append(barDictionary)

    return jsonify(allBarsDictionary)

# Delete Bar from Database
@apiEndpoints.route('/bars', methods=['DELETE'])
@expects_json(barDeleteSchema)
def del_bar():
    # Get Values from Request   
    values = request.get_json()

    # Initiate Database Cursor
    mycursor = connection.cursor()

    #Check if Row Exists 
    checkStatement = "SELECT * FROM Bars WHERE barName = '%s'" % (values["barName"])
    mycursor.execute(checkStatement)
    checkBars = mycursor.fetchall()
    if checkBars == []:
        # Make Response that Bar does not Exist
        returnString = "This Bar Does not Exist in the Database! <br> See existsing bars using the GET method on the /bars endpoint."
        response = make_response(returnString, 200)
        response.mimetype = "text/html"
        return(response)
    else:
        # Delete Bar from Database
        deleteStatement = "DELETE FROM Bars WHERE barName='%s'" % (values["barName"])
        mycursor.execute(deleteStatement)
        mycursor.close()
        connection.commit()

        # Make Response
        returnString = "Success! <b>%s</b> was deleted from the list of Bars. <br> Run a GET method on the /bars endpoint to see all Bars." % (values["barName"])
        response = make_response(returnString, 200)
        response.mimetype = "text/html"

        return(response)