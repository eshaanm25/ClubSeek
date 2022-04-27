from flask import Blueprint, request, jsonify, make_response
from flask_expects_json import expects_json
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

apiEndpoints = Blueprint('apiEndpoints',__name__)

from constants import *
from main import db

# Readiness Probe 
@apiEndpoints.route('/readiness', methods=['GET'])
def readiness():
    try:
        
        query = db.session.query(Bars).all()

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

    # Assemble Data to add to DB
    bar = Bars(
        address = values["address"],
        barName = values["barName"],
        capacity = values["capacity"],
        currentTraffic = values["currentTraffic"],
        wowFactor = values["wowFactor"]
    )

    try: 
        # Add Data to DB
        db.session.add(bar)
        db.session.commit()

        # Make Response
        returnString = "Success! <b>%s</b> was added to the list of Bars. <br> Run a GET method on the /bars endpoint to see all Bars." % (values["barName"])
        response = make_response(returnString, 200)
        response.mimetype = "text/html"
        return(response)

    except IntegrityError as e: 
        returnString = "The bar <b>%s</b> was already added to the list of Bars. <br><br> Error from Application: %s" % (values["barName"], e)
        response = make_response(returnString, 300)
        response.mimetype = "text/html"
        return(response)


# Get all Bars from Database
@apiEndpoints.route('/bars', methods=['GET'])
def get_bar():

    bars = db.session.query(Bars).all()

    if bars == []:
        # Make Response that Table is Empty
        returnString = "There are no Bars yet! <br> Add a bar using the POST method on the /bar endpoint. <br> See README for request body schema."
        response = make_response(returnString, 300)
        response.mimetype = "text/html"
        return(response)

 
    # Make Response with all Bars as a Dictionary
    allBarsDictionary = []
    for bar in bars:
        barDictionary = dict(barName = bar.barName, wowFactor=bar.wowFactor, capacity=bar.capacity,  currentTraffic=bar.currentTraffic, address=bar.address)
        allBarsDictionary.append(barDictionary)

    return jsonify(allBarsDictionary)

# Delete Bar from Database
@apiEndpoints.route('/bars', methods=['DELETE'])
@expects_json(barDeleteSchema)
def del_bar():
    # Get Values from Request   
    values = request.get_json()
    
    query = Bars.query.filter(Bars.barName == values["barName"]).filter(Bars.address == values["address"]).delete()
    db.session.commit()

    if query >= 1:
        # Make Response
        returnString = "Success! <b>%s</b> was deleted from the list of Bars. <br> Run a GET method on the /bars endpoint to see all Bars." % (values["barName"])
        response = make_response(returnString, 200)
        response.mimetype = "text/html"
        return(response)
    else:
        # Make Response that Bar does not Exist
        returnString = "This Bar Does not Exist in the Database! <br> See existing bars using the GET method on the /bars endpoint"
        response = make_response(returnString, 300)
        response.mimetype = "text/html"
        return(response)