from flask import Blueprint, request, jsonify, make_response
from flask_expects_json import expects_json
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from get_docker_secret import get_docker_secret
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
from helpers import *

apiEndpoints = Blueprint('apiEndpoints',__name__)

from constants import *
from main import db

auth = HTTPBasicAuth()
applicationCredentials = json.loads((get_docker_secret('application_credentials')))

print(applicationCredentials)


@auth.verify_password
def verify_password(username, password):
    if username in applicationCredentials and \
            check_password_hash(applicationCredentials.get(username), password):
        return username

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
@auth.login_required
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

        if bar["currentTraffic"] > bar["capacity"]:
            returnString = "The bar <b>%s</b> has more traffic than capacity. Please wait until the bar has lower traffic" % (bar["barName"])
            response = make_response(returnString, 400)
            response.mimetype = "text/html"
            return(response)

    try: 
        # Add Data to DB
        db.session.add_all(allBarObjects)
        db.session.commit()

        # Make Response
        returnString = "Success %s! Bars were added to the database. <br> Run a GET method on the /bars endpoint to see all Bars." % (auth.current_user())
        response = make_response(returnString, 200)
        response.mimetype = "text/html"
        return(response)

    except IntegrityError as e: 

        db.session.rollback()
        returnString = "One bar was already added to the list of Bars. <br><br> Error from Application: %s" % (e)
        response = make_response(returnString, 400)
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

    returnString = jsonify(allBarsDictionary)
    response = make_response(returnString, 200)
    response.mimetype = "application/json"
    return(response)

# Delete Bar from Database
@apiEndpoints.route('/bars', methods=['DELETE'])
@auth.login_required
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

# Bar Selection Algorithm
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
    
    # Process Preferences
    if bars != []:
        if "preference" in values:
            if values["preference"] == "wowFactor":
                bestBar = getGreatest(bars, "wowFactor")
            elif values["preference"] == "capacity":
                bestBar = getGreatest(bars, "capacity")
        else:
            response.append("Preference was not defined so it will default to capacity.")
            bestBar = getGreatest(bars, "capacity")


    if bestBar == None: 
        response.append("No Bars Met Your Requirements. Please Edit Your Request Attributes and Try Again.")
        returnString = ("<br>".join(response))
        return(createResponse(returnString, 300)) 
    else:
        
        # Add User to Users Table
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

        response.append("<b>%s</b> is the chosen bar based on your preferences! It has a WOW Factor of <b>%s</b> and is <b>%s%%</b> full. <br> The address is <b>%s</b>. Have fun <b>%s</b>!" % (bestBar.barName, bestBar.wowFactor, 100*round(bestBar.currentTraffic/bestBar.capacity, 2), bestBar.address, values["name"])) 
        returnString = ("<br>".join(response))
        return(createResponse(returnString, 200))


# Get all Users from Database
@apiEndpoints.route('/users', methods=['GET'])
@auth.login_required
def get_users():

    users = db.session.query(Users).all()

    if users == []:
        # Make Response that Table is Empty
        returnString = "There are no Users yet! <br> Add a bar using the GET method on the /barSelection endpoint. <br> See README for request body schema."
        response = make_response(returnString, 300)
        response.mimetype = "text/html"
        return(response)

 
    # Make Response with all Bars as a Dictionary
    allUsersDictionary = []
    for user in users:
        userDictionary = dict(userName = user.userName, wowuserPhoneNumberFactor=user.userPhoneNumber, assignedBarName=user.assignedBarName,  assignedBarAddress=user.assignedBarAddress)
        allUsersDictionary.append(userDictionary)

    returnString = jsonify(allUsersDictionary)
    response = make_response(returnString, 200)
    response.mimetype = "application/json"
    return(response)