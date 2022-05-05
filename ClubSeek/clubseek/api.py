from flask import Blueprint, request, jsonify, make_response
from flask_expects_json import expects_json
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import clubseek.helpers
import clubseek.constants
apiEndpoints = Blueprint('apiEndpoints',__name__)

'''
All API Endpoints for all CRUD Operations in Application
Request Schemas and Database Classes can be found in constants.py
'''

# Readiness Probe to validate if API Endpoint has Connection to DB
@apiEndpoints.route('/readiness', methods=['GET'])
def readiness():
    import clubseek.main
    try:
        query = clubseek.main.db.session.query(clubseek.main.Bars).all()

        # Make Successful Response if Query is Successful
        return(clubseek.helpers.createResponse("Ready", 200))

    except SQLAlchemyError as e:

        # Make Unsuccessful Response if there is no conection to DB
        returnString = "ClubSeek is waiting for the MySQL Database to start. Connection status: %s" % (e)
        return(clubseek.helpers.createResponse(returnString, 503))

# Add Bars to Database
@apiEndpoints.route('/bars', methods=['POST'])
@clubseek.helpers.auth.login_required # Protected Endpoint, requires AuthZ
@expects_json(clubseek.constants.barSchema) 
def add_bar():
    import clubseek.main
    # Get Values from Request 
    values = request.get_json()
    allBarObjects = []

    # Assemble Data to add to DB
    for bar in values:
        allBarObjects.append(
            clubseek.main.Bars(
                address = bar["address"],
                barName = bar["barName"],
                capacity = bar["capacity"],
                currentTraffic = bar["currentTraffic"],
                wowFactor = bar["wowFactor"]
            )) 

        # Check if Current Traffic of a Bar Exceeds its Reported Capacity
        if bar["currentTraffic"] > bar["capacity"]:
            returnString = "The bar <b>%s</b> has more traffic than capacity. Please wait until the bar has lower traffic" % (bar["barName"])
            return(clubseek.helpers.createResponse(returnString, 400))

    try: 
        # Add Data to DB
        clubseek.main.db.session.add_all(allBarObjects)
        clubseek.main.db.session.commit()

        # Make Response
        returnString = "Success %s! Bars were added to the database. <br> Run a GET method on the /bars endpoint to see all Bars." % (clubseek.helpers.auth.current_user())
        return(clubseek.helpers.createResponse(returnString, 200))

    except IntegrityError as e: 
        # Rollback Request if there is a Bar Entry Conflict
        clubseek.main.db.session.rollback()
        returnString = "One bar was already added to the list of Bars. <br><br> Error from Application: %s" % (e)
        return(clubseek.helpers.createResponse(returnString, 400))


# Update Bar in Database
@apiEndpoints.route('/bars', methods=['PUT'])
@expects_json(clubseek.constants.barUpdateSchema)
@clubseek.helpers.auth.login_required # Protected Endpoint, requires AuthZ
def update_bar():
    import clubseek.main
    # Get Values from Request 
    values = request.get_json()

    # Check if Current Traffic of a Bar Exceeds its Reported Capacity
    if values["currentTrafficChange"] > values["capacityChange"]:
        returnString = "The bar <b>%s</b> has more traffic than capacity. Please wait until the bar has lower traffic" % (values["barName"])
        return(clubseek.helpers.createResponse(returnString, 400))

    # Query DB for Bar to Update
    bar = clubseek.main.Bars.query.filter(clubseek.main.Bars.barName == values["barName"]).filter(clubseek.main.Bars.address == values["address"]).first()

    # Check for Empty Table
    if bar == None:
        # Make Response that Table is Empty
        returnString = "There are no Bars with this Name and Address <br> Add a bar using the POST method on the /bar endpoint. <br> See README for request body schema."
        return(clubseek.helpers.createResponse(returnString, 400))

    # Update Bar information
    if "wowFactorChange" in values:
        bar.wowFactor = values["wowFactorChange"]
    if "capacityChange" in values:
        bar.capacity = values["capacityChange"]
    if "currentTrafficChange" in values:
        bar.currentTraffic = values["currentTrafficChange"]
    
    clubseek.main.db.session.commit()

    # Make Successful Reponse 
    returnString = "Success %s! Bar was updated. <br> Run a GET method on the /bars endpoint to see all Bars." % (clubseek.helpers.auth.current_user())
    return(clubseek.helpers.createResponse(returnString, 200))

# Get all Bars from Database
@apiEndpoints.route('/bars', methods=['GET'])
def get_bar():
    import clubseek.main
    # Query DB for all Bars
    bars = clubseek.main.db.session.query(clubseek.main.Bars).all()

    # Check for Empty Table
    if bars == []:
        # Make Response that Table is Empty
        returnString = "There are no Bars yet! <br> Add a bar using the POST method on the /bar endpoint. <br> See README for request body schema."
        return(clubseek.helpers.createResponse(returnString, 211))

 
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
@clubseek.helpers.auth.login_required # Protected Endpoint, requires AuthZ
@expects_json(clubseek.constants.barDeleteSchema)
def del_bar():
    import clubseek.main
    # Get Values from Request   
    values = request.get_json()
    
    # Query to DB to Delete Bar
    query = clubseek.main.Bars.query.filter(clubseek.main.Bars.barName == values["barName"]).filter(clubseek.main.Bars.address == values["address"]).delete()
    clubseek.main.db.session.commit()

    # Check for Rows Affected. If 1, then a Bar was Deleted. If 0, the bar did Not Exist to Delete
    if query >= 1:
        # Make Response of Successful Deletion
        returnString = "Success! <b>%s</b> was deleted from the list of Bars. <br> Run a GET method on the /bars endpoint to see all Bars." % (values["barName"])
        return(clubseek.helpers.createResponse(returnString, 200))
    else:
        # Make Response that Bar does not Exist
        returnString = "This Bar Does not Exist in the Database! <br> See existing bars using the GET method on the /bars endpoint"
        return(clubseek.helpers.createResponse(returnString, 400))

# Bar Selection Algorithm. Chooses a Bar Based on Filters Provided in Input
@apiEndpoints.route('/barSelection', methods=['GET'])
@expects_json(clubseek.constants.barAlgorithmSchema)
def choose_bar():
    import clubseek.main
    # Get Values from Request   
    values = request.get_json()
    bestBar = None
    response = []
    
    # Query Databse for Minimum Requirements
    if "minWowFactor" in values and "maxTraffic" in values:
        bars = clubseek.main.Bars.query.filter(clubseek.main.Bars.wowFactor >= values["minWowFactor"]).filter(clubseek.main.Bars.currentTraffic <= values["maxTraffic"]).filter(clubseek.main.Bars.currentTraffic+1<=clubseek.main.Bars.capacity).all()
    elif "minWowFactor" in values:
        bars = clubseek.main.Bars.query.filter(clubseek.main.Bars.wowFactor >= values["minWowFactor"]).filter(clubseek.main.Bars.currentTraffic+1<=clubseek.main.Bars.capacity).all()
    elif "maxTraffic" in values:
        bars = clubseek.main.Bars.query.filter(clubseek.main.Bars.currentTraffic <= values["maxTraffic"]).filter(clubseek.main.Bars.currentTraffic+1<=clubseek.main.Bars.capacity).all()
    else:
        bars = clubseek.main.Bars.query.all()
    
    # Process Preference of Greatest WOW Factor or Lowest Capacity
    if bars != []:
        if "preference" in values:
            if values["preference"] == "wowFactor":
                bestBar = clubseek.helpers.getGreatestWow(bars)
            elif values["preference"] == "capacity":
                bestBar = clubseek.helpers.getLowestCapacity(bars)
        else:
            response.append("Preference was not defined so it will default to capacity.")
            bestBar = clubseek.helpers.getLowestCapacity(bars)

    # Return Message if No Bars Found for Filters
    if bestBar == None: 
        response.append("No Bars Met Your Requirements. Please Edit Your Request Attributes and Try Again.")
        returnString = ("<br>".join(response))
        return(clubseek.helpers.createResponse(returnString, 211)) 
    else:
        # Add User and Bar Selection to Users Table
        user = clubseek.main.Users(
            userName = values["name"],
            userPhoneNumber = values["phoneNumber"],
            assignedBarName = bestBar.barName,
            assignedBarAddress = bestBar.address
        )

        try: 
            clubseek.main.db.session.add(user)
            clubseek.main.db.session.commit()
        except IntegrityError as e: 
            clubseek.main.db.session.rollback()
            response.append("The user <b>%s</b> has already used the bar selection service. Usage is limited to once per day. <br><br> Error from Application: %s" % (values["name"], e))
            returnString = ("<br>".join(response))
            return(clubseek.helpers.createResponse(returnString, 400))
        
        # Add User to Current Traffic of Bar 
        bar = clubseek.main.Bars.query.filter(clubseek.main.Bars.barName == bestBar.barName).filter(clubseek.main.Bars.address == bestBar.address).first()
        bar.currentTraffic = bar.currentTraffic + 1
        clubseek.main.db.session.commit()

        # Return Response with Bar Details
        response.append("<b>%s</b> is the chosen bar based on your preferences! It has a WOW Factor of <b>%s</b> and is <b>%s%%</b> full. <br> The address is <b>%s</b>. Have fun <b>%s</b>!" % (bestBar.barName, bestBar.wowFactor, 100*round(bestBar.currentTraffic/bestBar.capacity, 2), bestBar.address, values["name"])) 
        returnString = ("<br>".join(response))
        return(clubseek.helpers.createResponse(returnString, 200))


# Get all Users from Database
@apiEndpoints.route('/users', methods=['GET'])
@clubseek.helpers.auth.login_required # Protected Endpoint, requires AuthZ
def get_users():
    import clubseek.main
    # Query DB for All Users
    users = clubseek.main.db.session.query(clubseek.main.Users).all()

    # Check for Empty Table
    if users == []:
        # Make Response that Table is Empty
        returnString = "There are no Users yet! <br> Add a bar using the GET method on the /barSelection endpoint. <br> See README for request body schema."
        return(clubseek.helpers.createResponse(returnString, 211))

    # Make Response with all Bars as a Dictionary
    allUsersDictionary = []
    for user in users:
        userDictionary = dict(userName = user.userName, wowuserPhoneNumberFactor=user.userPhoneNumber, assignedBarName=user.assignedBarName,  assignedBarAddress=user.assignedBarAddress)
        allUsersDictionary.append(userDictionary)

    returnString = jsonify(allUsersDictionary)
    response = make_response(returnString, 200)
    response.mimetype = "application/json"
    return(response)