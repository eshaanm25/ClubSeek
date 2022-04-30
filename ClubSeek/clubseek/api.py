from flask import Blueprint, request, jsonify, make_response
from flask_expects_json import expects_json
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from helpers import *
apiEndpoints = Blueprint('apiEndpoints',__name__)
from constants import *
from main import db

'''
All API Endpoints for all CRUD Operations in Application
Request Schemas and Database Classes can be found in constants.py
'''

# Readiness Probe to validate if API Endpoint has Connection to DB
@apiEndpoints.route('/readiness', methods=['GET'])
def readiness():
    try:
        query = db.session.query(Bars).all()

        # Make Successful Response if Query is Successful
        return(createResponse("Ready", 200))

    except SQLAlchemyError as e:

        # Make Unsuccessful Response if there is no conection to DB
        returnString = "ClubSeek is waiting for the MySQL Database to start. Connection status: %s" % (e)
        return(createResponse(returnString, 502))

# Add Bars to Database
@apiEndpoints.route('/bars', methods=['POST'])
@auth.login_required # Protected Endpoint, requires AuthZ
@expects_json(barSchema) 
def add_bar():
    # Get Values from Request 
    values = request.get_json()
    allBarObjects = []

    # Assemble Data to add to DB
    for bar in values:
        allBarObjects.append(
            Bars(
                address = bar["address"],
                barName = bar["barName"],
                capacity = bar["capacity"],
                currentTraffic = bar["currentTraffic"],
                wowFactor = bar["wowFactor"]
            )) 

        # Check if Current Traffic of a Bar Exceeds its Reported Capacity
        if bar["currentTraffic"] > bar["capacity"]:
            returnString = "The bar <b>%s</b> has more traffic than capacity. Please wait until the bar has lower traffic" % (bar["barName"])
            return(createResponse(returnString, 400))

    try: 
        # Add Data to DB
        db.session.add_all(allBarObjects)
        db.session.commit()

        # Make Response
        returnString = "Success %s! Bars were added to the database. <br> Run a GET method on the /bars endpoint to see all Bars." % (auth.current_user())
        return(createResponse(returnString, 200))

    except IntegrityError as e: 
        # Rollback Request if there is a Bar Entry Conflict
        db.session.rollback()
        returnString = "One bar was already added to the list of Bars. <br><br> Error from Application: %s" % (e)
        return(createResponse(returnString, 400))


# Update Bar in Database
@apiEndpoints.route('/bars', methods=['PUT'])
@expects_json(barUpdateSchema)
@auth.login_required # Protected Endpoint, requires AuthZ
def update_bar():
    
    # Get Values from Request 
    values = request.get_json()

    # Query DB for Bar to Update
    bar = Bars.query.filter(Bars.barName == values["barName"]).filter(Bars.address == values["address"]).first()

    # Check for Empty Table
    if bar == []:
        # Make Response that Table is Empty
        returnString = "There are no Bars with this Name and Address <br> Add a bar using the POST method on the /bar endpoint. <br> See README for request body schema."
        return(createResponse(returnString, 300))

    # Update Bar information
    if "wowFactorChange" in values:
        bar.wowFactor = values["wowFactorChange"]
    if "capacityChange" in values:
        bar.capacity = values["capacityChange"]
    if "currentTrafficChange" in values:
        bar.currentTraffic = values["currentTrafficChange"]
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        # Make Unsuccessful Response if unable to Update
        returnString = "ClubSeek is waiting for the MySQL Database to start. Connection status: %s" % (e)
        return(createResponse(returnString, 502))

    # Make Successful Reponse 
    returnString = "Success %s! Bar was updated. <br> Run a GET method on the /bars endpoint to see all Bars." % (auth.current_user())
    return(createResponse(returnString, 200))

# Get all Bars from Database
@apiEndpoints.route('/bars', methods=['GET'])
def get_bar():

    # Query DB for all Bars
    bars = db.session.query(Bars).all()

    # Check for Empty Table
    if bars == []:
        # Make Response that Table is Empty
        returnString = "There are no Bars yet! <br> Add a bar using the POST method on the /bar endpoint. <br> See README for request body schema."
        return(createResponse(returnString, 300))

 
    # Make Response with all Bars as a Dictionary
    allBarsDictionary = []
    for bar in bars:
        barDictionary = dict(barName = bar.barName, wowFactor=bar.wowFactor, capacity=bar.capacity,  currentTraffic=bar.currentTraffic, address=bar.address)
        allBarsDictionary.append(barDictionary)

    returnString = jsonify(allBarsDictionary)
    response = make_response(returnString, 200)
    response.mimetype = "application/json"
    return(response)

# Delete Bar from Database
@apiEndpoints.route('/bars', methods=['DELETE'])
@auth.login_required # Protected Endpoint, requires AuthZ
@expects_json(barDeleteSchema)
def del_bar():
    
    # Get Values from Request   
    values = request.get_json()
    
    # Query to DB to Delete Bar
    query = Bars.query.filter(Bars.barName == values["barName"]).filter(Bars.address == values["address"]).delete()
    db.session.commit()

    # Check for Rows Affected. If 1, then a Bar was Deleted. If 0, the bar did Not Exist to Delete
    if query >= 1:
        # Make Response of Successful Deletion
        returnString = "Success! <b>%s</b> was deleted from the list of Bars. <br> Run a GET method on the /bars endpoint to see all Bars." % (values["barName"])
        return(createResponse(returnString, 200))
    else:
        # Make Response that Bar does not Exist
        returnString = "This Bar Does not Exist in the Database! <br> See existing bars using the GET method on the /bars endpoint"
        return(createResponse(returnString, 300))

# Bar Selection Algorithm. Chooses a Bar Based on Filters Provided in Input
@apiEndpoints.route('/barSelection', methods=['GET'])
@expects_json(barAlgorithmSchema)
def choose_bar():
    # Get Values from Request   
    values = request.get_json()
    bestBar = None
    response = []
    
    # Query Databse for Minimum Requirements
    if "minWowFactor" in values and "maxTraffic" in values:
        bars = Bars.query.filter(Bars.wowFactor >= values["minWowFactor"]).filter(Bars.currentTraffic <= values["maxTraffic"]).filter(Bars.currentTraffic+1<=Bars.capacity).all()
    elif "minWowFactor" in values:
        bars = Bars.query.filter(Bars.wowFactor >= values["minWowFactor"]).filter(Bars.currentTraffic+1<=Bars.capacity).all()
    elif "maxTraffic" in values:
        bars = Bars.query.filter(Bars.currentTraffic <= values["maxTraffic"]).filter(Bars.currentTraffic+1<=Bars.capacity).all()
    else:
        bars = Bars.query.all()
    
    # Process Preference of Greatest WOW Factor or Lowest Capacity
    if bars != []:
        if "preference" in values:
            if values["preference"] == "wowFactor":
                bestBar = getGreatestWow(bars)
            elif values["preference"] == "capacity":
                bestBar = getLowestCapacity(bars)
        else:
            response.append("Preference was not defined so it will default to capacity.")
            bestBar = getLowestCapacity(bars)

    # Return Message if No Bars Found for Filters
    if bestBar == None: 
        response.append("No Bars Met Your Requirements. Please Edit Your Request Attributes and Try Again.")
        returnString = ("<br>".join(response))
        return(createResponse(returnString, 300)) 
    else:
        # Add User and Bar Selection to Users Table
        user = Users(
            userName = values["name"],
            userPhoneNumber = values["phoneNumber"],
            assignedBarName = bestBar.barName,
            assignedBarAddress = bestBar.address
        )

        try: 
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e: 
            db.session.rollback()
            response.append("The user <b>%s</b> has already used the bar selection service. Usage is limited to once per day. <br><br> Error from Application: %s" % (values["name"], e))
            returnString = ("<br>".join(response))
            return(createResponse(returnString, 400))
        
        # Add User to Current Traffic of Bar 
        bar = Bars.query.filter(Bars.barName == bestBar.barName).filter(Bars.address == bestBar.address).first()
        bar.currentTraffic = bar.currentTraffic + 1
        db.session.commit()

        # Return Response with Bar Details
        response.append("<b>%s</b> is the chosen bar based on your preferences! It has a WOW Factor of <b>%s</b> and is <b>%s%%</b> full. <br> The address is <b>%s</b>. Have fun <b>%s</b>!" % (bestBar.barName, bestBar.wowFactor, 100*round(bestBar.currentTraffic/bestBar.capacity, 2), bestBar.address, values["name"])) 
        returnString = ("<br>".join(response))
        return(createResponse(returnString, 200))


# Get all Users from Database
@apiEndpoints.route('/users', methods=['GET'])
@auth.login_required # Protected Endpoint, requires AuthZ
def get_users():

    # Query DB for All Users
    users = db.session.query(Users).all()

    # Check for Empty Table
    if users == []:
        # Make Response that Table is Empty
        returnString = "There are no Users yet! <br> Add a bar using the GET method on the /barSelection endpoint. <br> See README for request body schema."
        return(createResponse(returnString, 300))

    # Make Response with all Bars as a Dictionary
    allUsersDictionary = []
    for user in users:
        userDictionary = dict(userName = user.userName, wowuserPhoneNumberFactor=user.userPhoneNumber, assignedBarName=user.assignedBarName,  assignedBarAddress=user.assignedBarAddress)
        allUsersDictionary.append(userDictionary)

    returnString = jsonify(allUsersDictionary)
    response = make_response(returnString, 200)
    response.mimetype = "application/json"
    return(response)